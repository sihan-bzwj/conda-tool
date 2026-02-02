#!/usr/bin/env python3
"""
Conda 一站式清理与管理工具 / Conda All-in-One Cleanup & Management Tool
"""

import subprocess
import os
import sys
import re
import json
import locale

# ==================== 语言配置 / Language Configuration ====================
class I18N:
    def __init__(self, lang='zh'):
        self.lang = lang
        self.translations = {
            'zh': {
                # 主菜单 / Main Menu
                'menu_title': "Conda 一站式清理与管理工具",
                'menu_clean': "🧹 一键安全清理缓存（不删除环境）",
                'menu_env': "📁 查看与管理环境（可删除）",
                'menu_disk': "📊 查看磁盘占用情况",
                'menu_lang': "🌐 切换语言 (Switch to English)",
                'menu_exit': "🚪 退出",
                'menu_choice': "请选择操作 (1-5): ",
                'invalid_choice': "无效输入，请重新选择。",
                
                # 清理功能 / Cleaning Function
                'clean_title': "开始一键安全清理...",
                'clean_conda': "正在清理 Conda 包缓存...",
                'clean_pip': "正在清理 Pip 缓存...",
                'clean_done': "✅ 所有缓存清理完毕！",
                'clean_fail': "  跳过或失败",
                'clean_success': "  完成",
                
                # 环境管理 / Environment Management
                'env_fetching': "正在获取所有 Conda 环境...",
                'env_none': "未找到任何环境。",
                'env_found': "找到 {} 个环境:",
                'env_num': "序号",
                'env_status': "状态",
                'env_name': "环境名",
                'env_path': "路径",
                'env_current': " ✅ ",
                'env_inactive': "    ",
                'env_delete_prompt': "输入要删除的环境序号 (直接回车返回主菜单): ",
                'env_delete_confirm': "⚠️  确认删除环境 '{}' 吗？此操作不可逆！(输入 y 确认): ",
                'env_deleting': "正在删除 '{}'...",
                'env_deleted': "✅ 环境 '{}' 已删除。",
                'env_delete_failed': "❌ 删除失败，可能权限不足或环境已被删除。",
                'env_base_protected': "🚫 保护：禁止删除 base 根环境！",
                'env_current_protected': "🚫 无法删除当前正在使用的环境，请先切换到其他环境。",
                'env_invalid_index': "序号无效。",
                
                # 磁盘分析 / Disk Analysis
                'disk_analyzing': "📊 正在分析Anaconda主要目录大小（这可能需要几秒钟）...",
                'disk_not_found': "未找到Anaconda/Miniconada安装目录。",
                'disk_root': "安装根目录: {}",
                'disk_total': "💾 以上目录总计占用: {:.1f} MB",
                'disk_gb': "  约 {:.1f} GB",
                
                # 通用 / General
                'press_enter': "按 Enter 键返回主菜单...",
                'goodbye': "感谢使用，再见！",
                'interrupted': "程序被中断。",
                'conda_not_found': "❌ 未找到 conda 命令。请在 Anaconda Prompt 中运行此脚本。",
                'conda_press_exit': "按 Enter 键退出..."
            },
            'en': {
                # Main Menu
                'menu_title': "Conda All-in-One Cleanup & Management Tool",
                'menu_clean': "🧹 Safe One-click Cache Cleanup (no env deletion)",
                'menu_env': "📁 View & Manage Environments (deletion available)",
                'menu_disk': "📊 Check Disk Usage",
                'menu_lang': "🌐 切换语言 (切换到中文)",
                'menu_exit': "🚪 Exit",
                'menu_choice': "Select operation (1-5): ",
                'invalid_choice': "Invalid input, please try again.",
                
                # Cleaning Function
                'clean_title': "Starting safe one-click cleanup...",
                'clean_conda': "Cleaning Conda package cache...",
                'clean_pip': "Cleaning Pip cache...",
                'clean_done': "✅ All cache cleaned successfully!",
                'clean_fail': "  Skipped or failed",
                'clean_success': "  Done",
                
                # Environment Management
                'env_fetching': "Fetching all Conda environments...",
                'env_none': "No environments found.",
                'env_found': "Found {} environment(s):",
                'env_num': "No.",
                'env_status': "Status",
                'env_name': "Env Name",
                'env_path': "Path",
                'env_current': " ✅ ",
                'env_inactive': "    ",
                'env_delete_prompt': "Enter environment number to delete (Enter to return): ",
                'env_delete_confirm': "⚠️  Confirm deletion of '{}'? This is irreversible! (type y to confirm): ",
                'env_deleting': "Deleting '{}'...",
                'env_deleted': "✅ Environment '{}' deleted.",
                'env_delete_failed': "❌ Deletion failed, possibly insufficient permissions.",
                'env_base_protected': "🚫 Protection: Cannot delete base root environment!",
                'env_current_protected': "🚫 Cannot delete current active environment. Switch first.",
                'env_invalid_index': "Invalid index number.",
                
                # Disk Analysis
                'disk_analyzing': "📊 Analyzing Anaconda directory sizes (may take a few seconds)...",
                'disk_not_found': "Anaconda/Miniconada installation not found.",
                'disk_root': "Installation root: {}",
                'disk_total': "💾 Total disk usage: {:.1f} MB",
                'disk_gb': "  Approximately {:.1f} GB",
                
                # General
                'press_enter': "Press Enter to return to main menu...",
                'goodbye': "Thank you for using, goodbye!",
                'interrupted': "Program interrupted.",
                'conda_not_found': "❌ Conda command not found. Please run in Anaconda Prompt.",
                'conda_press_exit': "Press Enter to exit..."
            }
        }
    
    def t(self, key, *args):
        """获取翻译 / Get translation"""
        text = self.translations[self.lang].get(key, key)
        if args:
            try:
                return text.format(*args)
            except:
                return text
        return text
    
    def switch_language(self):
        """切换语言 / Switch language"""
        self.lang = 'en' if self.lang == 'zh' else 'zh'
        return self.lang

# ==================== 核心功能 / Core Functions ====================
def run_cmd(cmd):
    """执行命令 / Execute command"""
    try:
        subprocess.run(cmd, shell=True, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def clean_all_cache(i18n):
    """功能1：一键清理所有缓存 / Clean all cache"""
    print(f"\n{i18n.t('clean_title')}")
    print("-" * 50)
    
    steps = [
        (i18n.t('clean_conda'), "conda clean --all -y"),
        (i18n.t('clean_pip'), "pip cache purge"),
    ]
    
    for desc, cmd in steps:
        print(desc)
        if run_cmd(cmd):
            print(i18n.t('clean_success'))
        else:
            print(i18n.t('clean_fail'))
    
    print("-" * 50)
    print(i18n.t('clean_done'))
    input(f"\n{i18n.t('press_enter')}")

def list_and_manage_envs(i18n):
    """功能2：列出并管理环境 / List and manage environments"""
    print(f"\n{i18n.t('env_fetching')}")
    result = subprocess.run("conda env list", shell=True, 
                          capture_output=True, text=True, encoding='utf-8')
    lines = result.stdout.strip().split('\n')
    
    envs = []
    for line in lines:
        match = re.search(r'^(\S+)\s+(\*.+|\S+)', line)
        if match and not line.startswith('#'):
            name, path = match.groups()
            is_current = '*' in path
            path = path.replace('*', '').strip()
            envs.append({"name": name, "path": path, "current": is_current})
    
    if not envs:
        print(i18n.t('env_none'))
        input(f"\n{i18n.t('press_enter')}")
        return
    
    # 显示列表 / Display list
    print(f"\n{i18n.t('env_found', len(envs))}\n")
    print(f"{i18n.t('env_num'):<4} {i18n.t('env_status'):<6} {i18n.t('env_name'):<20} {i18n.t('env_path')}")
    print("-" * 60)
    
    for i, env in enumerate(envs, 1):
        status = i18n.t('env_current') if env["current"] else i18n.t('env_inactive')
        print(f"{i:<4} {status:<6} {env['name']:<20} {env['path']}")
    
    # 删除操作 / Deletion operation
    print("\n" + "=" * 60)
    choice = input(i18n.t('env_delete_prompt')).strip()
    
    if choice and choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(envs):
            target_env = envs[idx]
            
            if target_env["name"] == "base":
                print(i18n.t('env_base_protected'))
            elif target_env["current"]:
                print(i18n.t('env_current_protected'))
            else:
                confirm = input(i18n.t('env_delete_confirm', target_env['name']))
                if confirm.lower() == 'y':
                    print(i18n.t('env_deleting', target_env['name']))
                    if run_cmd(f"conda remove -n {target_env['name']} --all -y"):
                        print(i18n.t('env_deleted', target_env['name']))
                    else:
                        print(i18n.t('env_delete_failed'))
        else:
            print(i18n.t('env_invalid_index'))
    
    input(f"\n{i18n.t('press_enter')}")

def show_disk_usage(i18n):
    """功能3：查看磁盘占用 / Check disk usage"""
    print(f"\n{i18n.t('disk_analyzing')}")
    
    possible_paths = [
        os.path.expanduser("~/anaconda3"),
        os.path.expanduser("~/miniconda3"),
        os.path.expanduser("~/AppData/Local/Continuum/anaconda3"),
        "C:\\ProgramData\\Anaconda3",
    ]
    
    conda_path = None
    for path in possible_paths:
        if os.path.exists(path):
            conda_path = path
            break
    
    if not conda_path:
        print(i18n.t('disk_not_found'))
    else:
        print(i18n.t('disk_root', conda_path))
        total_size = 0
        
        for dir_name in ['envs', 'pkgs']:
            dir_path = os.path.join(conda_path, dir_name)
            if os.path.exists(dir_path):
                dir_size = 0
                for root, dirs, files in os.walk(dir_path):
                    for f in files:
                        try:
                            fp = os.path.join(root, f)
                            dir_size += os.path.getsize(fp)
                        except:
                            pass
                size_mb = dir_size / (1024 * 1024)
                total_size += dir_size
                print(f"  {dir_name}: {size_mb:.1f} MB")
        
        total_mb = total_size / (1024 * 1024)
        print(f"\n{i18n.t('disk_total', total_mb)}")
        if total_mb > 1024:
            print(i18n.t('disk_gb', total_mb/1024))
    
    input(f"\n{i18n.t('press_enter')}")

def save_language_config(lang):
    """保存语言配置 / Save language configuration"""
    config = {'language': lang}
    config_path = os.path.expanduser('~/.conda_tool_config.json')
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f)
    except:
        pass

def load_language_config():
    """加载语言配置 / Load language configuration"""
    config_path = os.path.expanduser('~/.conda_tool_config.json')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('language', 'zh')
        except:
            return 'zh'
    return 'zh'

# ==================== 主程序 / Main Program ====================
def main():
    # 加载语言配置 / Load language config
    lang = load_language_config()
    i18n = I18N(lang)
    
    # 检查conda / Check conda
    if not run_cmd("conda --version"):
        print(i18n.t('conda_not_found'))
        input(i18n.t('conda_press_exit'))
        sys.exit(1)
    
    while True:
        # 清屏 / Clear screen
        os.system('cls' if sys.platform == 'win32' else 'clear')
        
        # 显示菜单 / Display menu
        print("\n" + "=" * 60)
        print(f"        {i18n.t('menu_title')}")
        print("=" * 60)
        print(f"  1. {i18n.t('menu_clean')}")
        print(f"  2. {i18n.t('menu_env')}")
        print(f"  3. {i18n.t('menu_disk')}")
        print(f"  4. {i18n.t('menu_lang')}")
        print(f"  5. {i18n.t('menu_exit')}")
        print("-" * 60)
        
        choice = input(i18n.t('menu_choice')).strip()
        
        if choice == "1":
            clean_all_cache(i18n)
        elif choice == "2":
            list_and_manage_envs(i18n)
        elif choice == "3":
            show_disk_usage(i18n)
        elif choice == "4":
            # 切换语言 / Switch language
            new_lang = i18n.switch_language()
            save_language_config(new_lang)
            i18n = I18N(new_lang)
            print(f"\n✅ Language switched to {'English' if new_lang == 'en' else 'Chinese'}")
            input(f"\n{i18n.t('press_enter')}")
        elif choice == "5":
            print(f"\n{i18n.t('goodbye')}")
            sys.exit(0)
        else:
            print(i18n.t('invalid_choice'))
            input(f"\n{i18n.t('press_enter')}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{I18N(load_language_config()).t('interrupted')}")
        sys.exit(0)