#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地文件上传脚本
用于将本地文件上传到moi平台的指定连接器
"""

import requests
import sys
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
import mimetypes
from config import get_moi_key_interactive, get_base_url


def upload_file(
    file_path: str,
    volume_id: str,
    moi_key: Optional[str] = None,
    base_url: str = get_base_url()
) -> Dict[str, Any]:
    """
    上传单个文件到平台
    
    参数:
        file_path (str): 本地文件路径
        volume_id (str): 目标数据卷ID
        moi_key (str): API密钥，如果不提供将提示输入
        base_url (str): API基础URL
    
    返回:
        Dict[str, Any]: API响应结果
    """
    
    # 验证文件是否存在
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    if not os.path.isfile(file_path):
        raise ValueError(f"路径不是文件: {file_path}")
    
    # 如果没有提供API密钥，提示用户输入
    if not moi_key:
        moi_key = get_moi_key_interactive()
        if not moi_key:
            raise ValueError("moi-key 不能为空")
    
    # 构建请求URL
    url = f"{base_url}/connectors/upload"
    
    # 构建请求头（注意：multipart/form-data的Content-Type会由requests自动设置）
    headers = {
        "Moi-Key": moi_key
    }
    
    # 获取文件信息
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    mime_type, _ = mimetypes.guess_type(file_path)
    
    try:
        print(f"正在上传文件: {file_name}")
        print(f"文件大小: {format_file_size(file_size)}")
        print(f"目标数据卷ID: {volume_id}")
        print("-" * 50)
        
        # 准备元数据（meta参数是必需的，需要是数组格式）
        meta = json.dumps([{
            "file_name": file_name,
            "file_size": file_size,
            "mime_type": mime_type or "application/octet-stream"
        }])
        
        # 准备文件和表单数据
        with open(file_path, 'rb') as f:
            files = {
                "file": (file_name, f, mime_type or "application/octet-stream")
            }
            
            data = {
                "VolumeID": volume_id,
                "meta": meta
            }
            
            # 发送POST请求
            response = requests.post(url, headers=headers, files=files, data=data)
        
        # 检查HTTP状态码
        response.raise_for_status()
        
        # 解析JSON响应
        result = response.json()
        
        print("✅ 文件上传成功!")
        
        # 格式化显示上传结果
        if 'data' in result:
            data = result['data']
            print(f"\n📊 上传结果:")
            print("=" * 50)
            print(f"成功: {data.get('success', False)}")
            print(f"文件ID: {data.get('file_id', 'N/A')}")
            print(f"任务ID: {data.get('task_id', 'N/A')}")
            print(f"消息: {data.get('message', 'N/A')}")
            
            # 显示详细结果
            if 'results' in data and data['results']:
                print(f"\n📋 详细结果:")
                for i, file_result in enumerate(data['results'], 1):
                    print(f"[{i}] 文件上传结果:")
                    print(f"    成功: {file_result.get('success', False)}")
                    print(f"    文件ID: {file_result.get('file_id', 'N/A')}")
                    print(f"    消息: {file_result.get('message', 'N/A')}")
                    print("-" * 30)
        
        print(f"\n🔍 完整响应结果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                print(f"错误详情: {json.dumps(error_detail, indent=2, ensure_ascii=False)}")
            except:
                print(f"错误详情: {e.response.text}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 发生未知错误: {e}")
        sys.exit(1)


def batch_upload_files(
    file_paths: List[str],
    volume_id: str,
    moi_key: Optional[str] = None,
    base_url: str = get_base_url()
) -> List[Dict[str, Any]]:
    """
    批量上传多个文件
    
    参数:
        file_paths (List[str]): 文件路径列表
        volume_id (str): 目标数据卷ID
        moi_key (str): API密钥
        base_url (str): API基础URL
    
    返回:
        List[Dict[str, Any]]: 上传结果列表
    """
    results = []
    total_files = len(file_paths)
    
    print(f"📁 开始批量上传 {total_files} 个文件")
    print("=" * 60)
    
    for i, file_path in enumerate(file_paths, 1):
        try:
            print(f"\n[{i}/{total_files}] 正在处理: {os.path.basename(file_path)}")
            result = upload_file(
                file_path=file_path,
                volume_id=volume_id,
                moi_key=moi_key,
                base_url=base_url
            )
            results.append({
                'file_path': file_path,
                'success': True,
                'result': result
            })
        except Exception as e:
            print(f"❌ 文件上传失败: {file_path}")
            print(f"错误: {e}")
            results.append({
                'file_path': file_path,
                'success': False,
                'error': str(e)
            })
    
    # 显示批量上传统计
    successful_uploads = sum(1 for r in results if r['success'])
    failed_uploads = total_files - successful_uploads
    
    print(f"\n📊 批量上传完成统计:")
    print("=" * 50)
    print(f"总文件数: {total_files}")
    print(f"成功上传: {successful_uploads}")
    print(f"失败上传: {failed_uploads}")
    print(f"成功率: {successful_uploads/total_files*100:.1f}%")
    
    return results


def upload_directory(
    directory_path: str,
    volume_id: str,
    file_extensions: Optional[List[str]] = None,
    recursive: bool = True,
    moi_key: Optional[str] = None,
    base_url: str = get_base_url()
) -> List[Dict[str, Any]]:
    """
    上传目录中的文件
    
    参数:
        directory_path (str): 目录路径
        volume_id (str): 目标数据卷ID
        file_extensions (List[str]): 允许的文件扩展名列表，如 ['.txt', '.pdf']
        recursive (bool): 是否递归子目录
        moi_key (str): API密钥
        base_url (str): API基础URL
    
    返回:
        List[Dict[str, Any]]: 上传结果列表
    """
    
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"目录不存在: {directory_path}")
    
    if not os.path.isdir(directory_path):
        raise ValueError(f"路径不是目录: {directory_path}")
    
    # 收集要上传的文件
    file_paths = []
    directory = Path(directory_path)
    
    if recursive:
        pattern = "**/*"
    else:
        pattern = "*"
    
    for file_path in directory.glob(pattern):
        if file_path.is_file():
            # 检查文件扩展名
            if file_extensions:
                if file_path.suffix.lower() in [ext.lower() for ext in file_extensions]:
                    file_paths.append(str(file_path))
            else:
                file_paths.append(str(file_path))
    
    if not file_paths:
        print("❌ 没有找到符合条件的文件")
        return []
    
    print(f"📁 找到 {len(file_paths)} 个文件准备上传")
    if file_extensions:
        print(f"文件类型过滤: {file_extensions}")
    print(f"递归模式: {'是' if recursive else '否'}")
    
    # 批量上传文件
    return batch_upload_files(
        file_paths=file_paths,
        volume_id=volume_id,
        moi_key=moi_key,
        base_url=base_url
    )


def format_file_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


def get_file_list_from_input() -> List[str]:
    """从用户输入获取文件列表"""
    file_paths = []
    print("请输入文件路径（输入空行结束）:")
    
    while True:
        file_path = input("文件路径: ").strip()
        if not file_path:
            break
        
        if os.path.exists(file_path) and os.path.isfile(file_path):
            file_paths.append(file_path)
            print(f"✅ 已添加: {os.path.basename(file_path)}")
        else:
            print(f"❌ 文件不存在或不是文件: {file_path}")
    
    return file_paths


def main():
    """主函数"""
    print("=" * 60)
    print("           moi - 本地文件上传脚本")
    print("=" * 60)
    
    try:
        # 选择上传模式
        print("\n请选择上传模式:")
        print("1. 单个文件上传")
        print("2. 批量文件上传") 
        print("3. 目录上传")
        
        mode = input("\n请输入模式编号 (1-3): ").strip()
        
        if mode not in ['1', '2', '3']:
            print("❌ 无效的模式选择")
            sys.exit(1)
        
        # 获取目标数据卷ID
        volume_id = input("请输入目标数据卷ID: ").strip()
        if not volume_id:
            print("❌ 数据卷ID不能为空")
            sys.exit(1)
        
        # 获取API密钥
        moi_key = get_moi_key_interactive()
        if not moi_key:
            print("❌ moi-key不能为空")
            sys.exit(1)
        
        if mode == '1':
            # 单个文件上传
            file_path = input("请输入文件路径: ").strip()
            if not file_path:
                print("❌ 文件路径不能为空")
                sys.exit(1)
            
            upload_file(
                file_path=file_path,
                volume_id=volume_id,
                moi_key=moi_key
            )
            
        elif mode == '2':
            # 批量文件上传
            file_paths = get_file_list_from_input()
            if not file_paths:
                print("❌ 没有有效的文件路径")
                sys.exit(1)
            
            batch_upload_files(
                file_paths=file_paths,
                volume_id=volume_id,
                moi_key=moi_key
            )
            
        elif mode == '3':
            # 目录上传
            directory_path = input("请输入目录路径: ").strip()
            if not directory_path:
                print("❌ 目录路径不能为空")
                sys.exit(1)
            
            # 文件类型过滤
            extensions_input = input("请输入允许的文件扩展名（用逗号分隔，如 .txt,.pdf，留空表示所有文件）: ").strip()
            file_extensions = None
            if extensions_input:
                file_extensions = [ext.strip() for ext in extensions_input.split(',')]
                print(f"文件类型过滤: {file_extensions}")
            
            # 递归选项
            recursive_input = input("是否递归子目录？(y/N): ").strip().lower()
            recursive = recursive_input in ['y', 'yes']
            
            upload_directory(
                directory_path=directory_path,
                volume_id=volume_id,
                file_extensions=file_extensions,
                recursive=recursive,
                moi_key=moi_key
            )
        
    except KeyboardInterrupt:
        print("\n\n👋 操作已取消")
        sys.exit(0)
    except Exception as e:
        print(f"❌ 程序执行失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()