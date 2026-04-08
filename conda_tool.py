import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import subprocess
import os
import json
import threading
import time
import signal
import sys

class CondaVisualProApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conda 进阶可视化控制台 (Pro)")
        self.root.geometry("900x650")
        
        self.is_busy = False
        self.current_process = None # 保存当前运行的 Popen 对象
        self.last_refresh_time = 0  # 用于防抖
        
        self.setup_ui()
        self.load_envs(silent=False)
        
        # 绑定窗口焦点获取事件，实现状态自动同步
        self.root.bind("<FocusIn>", self.on_window_focus)

    def setup_ui(self):
        # --- 顶部工具栏 ---
        self.toolbar = ttk.Frame(self.root)
        self.toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        ttk.Button(self.toolbar, text="🔄 刷新列表", command=lambda: self.load_envs(False)).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar, text="🧹 清理缓存", command=self.action_clean).pack(side=tk.LEFT, padx=2)
        
        # 中断按钮（红色警告色），默认禁用
        self.btn_kill = ttk.Button(self.toolbar, text="🛑 中止当前任务", command=self.kill_process, state=tk.DISABLED)
        self.btn_kill.pack(side=tk.RIGHT, padx=2)

        # --- 中部内容区 (左右分栏) ---
        self.main_pane = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 左侧：环境列表
        self.env_frame = ttk.LabelFrame(self.main_pane, text="环境列表 (Environments)")
        self.main_pane.add(self.env_frame, weight=3)
        
        cols = ('status', 'name', 'path')
        self.tree = ttk.Treeview(self.env_frame, columns=cols, show='headings', selectmode='browse')
        self.tree.heading('status', text="状态")
        self.tree.column('status', width=50, anchor='center')
        self.tree.heading('name', text="环境名")
        self.tree.column('name', width=150)
        self.tree.heading('path', text="路径")
        
        scroll = ttk.Scrollbar(self.env_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # 右侧：操作面板
        self.action_frame = ttk.Frame(self.main_pane)
        self.main_pane.add(self.action_frame, weight=1)
        
        ttk.Button(self.action_frame, text="➕ 新建环境", command=self.action_create).pack(fill=tk.X, pady=5)
        ttk.Button(self.action_frame, text="🗑️ 删除选中", command=self.action_delete).pack(fill=tk.X, pady=5)
        ttk.Button(self.action_frame, text="✏️ 重命名选中", command=self.action_rename).pack(fill=tk.X, pady=5)
        ttk.Button(self.action_frame, text="📦 安装依赖包", command=self.action_install).pack(fill=tk.X, pady=5)

        # --- 底部控制台 (解决黑盒化排错断层) ---
        self.console_frame = ttk.LabelFrame(self.root, text="终端输出日志 (Console)")
        self.console_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False, padx=5, pady=5)
        self.console_frame.configure(height=200)
        self.root.update() # 强制刷新布局
        
        self.console_text = tk.Text(self.console_frame, height=10, bg="black", fg="#00FF00", font=("Consolas", 10))
        self.console_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        console_scroll = ttk.Scrollbar(self.console_frame, orient=tk.VERTICAL, command=self.console_text.yview)
        self.console_text.configure(yscroll=console_scroll.set)
        console_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    # ==================== 核心进程管理与 I/O 监听 ====================
    def log(self, message, color="#00FF00"):
        """向底部控制台安全地写入日志"""
        self.console_text.config(state=tk.NORMAL)
        self.console_text.insert(tk.END, message + "\n")
        self.console_text.see(tk.END) # 自动滚动到底部
        self.console_text.config(state=tk.DISABLED)
        self.root.update_idletasks()

    def set_busy(self, busy_state):
        """统一管理 UI 锁定状态"""
        self.is_busy = busy_state
        self.btn_kill.config(state=tk.NORMAL if busy_state else tk.DISABLED)
        self.root.config(cursor="watch" if busy_state else "")

    def kill_process(self):
        """强制连根拔起底层子进程 (解决挂起与僵尸进程)"""
        if self.current_process and self.current_process.poll() is None:
            self.log("[!] 正在发送中断信号...", color="red")
            try:
                if sys.platform == 'win32':
                    # Windows下使用 CTRL_BREAK_EVENT 杀死整个进程组
                    os.kill(self.current_process.pid, signal.CTRL_BREAK_EVENT)
                else:
                    self.current_process.terminate()
            except Exception as e:
                self.log(f"[!] 进程终止异常: {e}")

    def run_action_stream(self, cmd, success_callback=None):
        """执行长时间任务，并实时捕获输出至控制台 (解决黑盒化)"""
        if self.is_busy:
            messagebox.showwarning("警告", "当前有任务正在运行，请等待或中止。")
            return
            
        self.set_busy(True)
        self.console_text.config(state=tk.NORMAL)
        self.console_text.delete(1.0, tk.END) # 清空旧日志
        self.console_text.config(state=tk.DISABLED)
        self.log(f"[$] 执行命令: {cmd}\n{'-'*50}")

        def task_thread():
            try:
                # 跨平台隐藏黑窗口与进程组隔离
                kwargs = {'shell': True, 'stdout': subprocess.PIPE, 'stderr': subprocess.STDOUT, 'text': True}
                if sys.platform == 'win32':
                    kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP
                
                self.current_process = subprocess.Popen(cmd, **kwargs)
                
                # 实时读取输出流
                for line in iter(self.current_process.stdout.readline, ''):
                    if line:
                        self.root.after(0, self.log, line.rstrip("\n"))
                
                self.current_process.stdout.close()
                return_code = self.current_process.wait()
                
                if return_code == 0:
                    self.root.after(0, self.log, f"\n[✓] 任务成功完成！")
                    if success_callback:
                        self.root.after(0, success_callback)
                else:
                    self.root.after(0, self.log, f"\n[X] 任务失败或被强行中止，退出码: {return_code}")
                    
            except Exception as e:
                self.root.after(0, self.log, f"\n[!] 发生严重错误: {str(e)}")
            finally:
                self.root.after(0, self.set_busy, False)
                self.current_process = None

        threading.Thread(target=task_thread, daemon=True).start()

    # ==================== 状态同步机制 ====================
    def on_window_focus(self, event):
        """焦点激活防抖更新 (解决状态同步延迟)"""
        if self.is_busy: return
        now = time.time()
        # 限制每 5 秒最多触发一次静默刷新
        if now - self.last_refresh_time > 5:
            self.load_envs(silent=True)

    def load_envs(self, silent=False):
        """拉取环境列表 (快速请求，使用 run 阻塞即可)"""
        if self.is_busy: return
        
        if not silent: self.log("[$] 正在拉取最新的环境列表...")
        self.last_refresh_time = time.time()
        
        def task():
            try:
                kwargs = {'shell': True, 'capture_output': True, 'text': True}
                if sys.platform == 'win32':
                    kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
                    
                result = subprocess.run("conda env list --json", **kwargs)
                if result.returncode == 0:
                    data = json.loads(result.stdout)
                    self.root.after(0, self._update_tree, data)
                    if not silent: self.root.after(0, self.log, "[✓] 列表更新完毕。")
            except Exception as e:
                if not silent: self.root.after(0, self.log, f"[!] 拉取列表失败: {e}")
                
        threading.Thread(target=task, daemon=True).start()

    def _update_tree(self, data):
        self.tree.delete(*self.tree.get_children())
        envs = data.get('envs', [])
        for env_path in envs:
            name = os.path.basename(env_path)
            # 基础环境判定
            status = "✅" if name.lower() in ['base', 'anaconda3', 'miniconda3'] else "" 
            self.tree.insert('', tk.END, values=(status, name, env_path))

    # ==================== 业务操作分支 ====================
    def get_selected_env(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("提示", "请先在左侧列表中点击选择一个环境。")
            return None
        return self.tree.item(selected[0])['values'][1]

    def action_clean(self):
        self.run_action_stream("conda clean --all -y")

    def action_create(self):
        name = simpledialog.askstring("新建环境", "请输入新环境名称:")
        if name:
            self.run_action_stream(f"conda create -n {name} -y", success_callback=lambda: self.load_envs(True))

    def action_delete(self):
        name = self.get_selected_env()
        if name and messagebox.askyesno("危险操作", f"确定要彻底删除环境 '{name}' 吗？\n此操作不可逆！"):
            self.run_action_stream(f"conda remove -n {name} --all -y", success_callback=lambda: self.load_envs(True))

    def action_rename(self):
        old_name = self.get_selected_env()
        if old_name:
            new_name = simpledialog.askstring("重命名", f"请输入 '{old_name}' 的新名称:\n(要求 Conda >= 23.3.0)")
            if new_name:
                self.run_action_stream(f"conda rename -n {old_name} {new_name}", success_callback=lambda: self.load_envs(True))

    def action_install(self):
        name = self.get_selected_env()
        if name:
            pkgs = simpledialog.askstring("安装依赖", f"目标环境: {name}\n请输入包名 (以空格分隔):")
            if pkgs:
                self.run_action_stream(f"conda install -n {name} {pkgs} -y")

if __name__ == "__main__":
    root = tk.Tk()
    app = CondaVisualProApp(root)
    root.mainloop()