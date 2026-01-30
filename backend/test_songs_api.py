"""
歌曲 API 测试脚本
运行前请确保：
1. 已创建 songs 表
2. 已插入测试数据
3. Flask 服务器正在运行
"""

import requests
import json

BASE_URL = "http://localhost:5000/api/songs"

def test_get_songs_list():
    """测试获取歌曲列表"""
    print("\n=== 测试：获取歌曲列表 ===")
    response = requests.get(f"{BASE_URL}/list?page=1&per_page=5")
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"返回数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
    return response.status_code == 200

def test_get_song_detail():
    """测试获取歌曲详情"""
    print("\n=== 测试：获取歌曲详情 ===")
    response = requests.get(f"{BASE_URL}/1")
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"返回数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
    return response.status_code == 200

def test_search_songs():
    """测试搜索歌曲"""
    print("\n=== 测试：搜索歌曲 ===")
    response = requests.get(f"{BASE_URL}/search?keyword=周杰伦")
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"返回数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
    return response.status_code == 200

def test_get_hot_songs():
    """测试获取热门歌曲"""
    print("\n=== 测试：获取热门歌曲 ===")
    response = requests.get(f"{BASE_URL}/hot?limit=5")
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"返回数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
    return response.status_code == 200

def test_get_latest_songs():
    """测试获取最新歌曲"""
    print("\n=== 测试：获取最新歌曲 ===")
    response = requests.get(f"{BASE_URL}/latest?limit=5")
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"返回数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
    return response.status_code == 200

def test_increment_play_count():
    """测试增加播放次数"""
    print("\n=== 测试：增加播放次数 ===")
    response = requests.post(f"{BASE_URL}/1/play")
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"返回数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
    return response.status_code == 200

def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("开始测试歌曲 API")
    print("=" * 50)
    
    tests = [
        ("获取歌曲列表", test_get_songs_list),
        ("获取歌曲详情", test_get_song_detail),
        ("搜索歌曲", test_search_songs),
        ("获取热门歌曲", test_get_hot_songs),
        ("获取最新歌曲", test_get_latest_songs),
        ("增加播放次数", test_increment_play_count),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, "✓ 通过" if success else "✗ 失败"))
        except Exception as e:
            results.append((name, f"✗ 错误: {str(e)}"))
    
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    for name, result in results:
        print(f"{name}: {result}")
    print("=" * 50)

if __name__ == "__main__":
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("\n错误：无法连接到服务器")
        print("请确保 Flask 服务器正在运行 (python app.py)")
