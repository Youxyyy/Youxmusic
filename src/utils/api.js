// API基础URL - 使用代理，不需要完整URL
const API_BASE_URL = '/api'

// 获取token
function getToken() {
  return localStorage.getItem('access_token')
}

// 通用请求函数
async function request(url, options = {}) {
  const token = getToken()
  
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  }
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  
  try {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      ...options,
      headers
    })
    
    const data = await response.json()
    
    if (!response.ok) {
      throw new Error(data.error || '请求失败')
    }
    
    return data
  } catch (error) {
    console.error('API请求错误:', error)
    throw error
  }
}

// 认证相关API
export const authAPI = {
  // 注册
  register(userData) {
    return request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData)
    })
  },
  
  // 登录
  login(credentials) {
    return request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials)
    })
  },
  
  // 获取当前用户信息
  getCurrentUser() {
    return request('/auth/me')
  },
  
  // 上传头像
  uploadAvatar(file) {
    const token = getToken()
    const formData = new FormData()
    formData.append('avatar', file)
    
    return fetch(`${API_BASE_URL}/auth/upload-avatar`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    }).then(res => res.json())
  },
  
  // 登出
  logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
  }
}

// 用户相关API
export const userAPI = {
  // 获取用户信息
  getUser(userId) {
    return request(`/user/${userId}`)
  },
  
  // 更新用户资料
  updateProfile(userData) {
    return request('/user/profile', {
      method: 'PUT',
      body: JSON.stringify(userData)
    })
  },
  
  // 获取用户统计
  getUserStats() {
    return request('/user/stats')
  }
}

// 歌曲相关API
export const songAPI = {
  // 获取歌曲列表
  getSongs(page = 1, perPage = 20) {
    return request(`/songs/list?page=${page}&per_page=${perPage}`)
  },
  
  // 获取歌曲详情
  getSong(songId) {
    return request(`/songs/${songId}`)
  },
  
  // 搜索歌曲
  searchSongs(keyword, page = 1, perPage = 20) {
    return request(`/songs/search?keyword=${keyword}&page=${page}&per_page=${perPage}`)
  },
  
  // 获取热门歌曲
  getHotSongs(limit = 10) {
    return request(`/songs/hot?limit=${limit}`)
  },
  
  // 获取最新歌曲
  getLatestSongs(limit = 10) {
    return request(`/songs/latest?limit=${limit}`)
  },
  
  // 增加播放次数
  incrementPlayCount(songId) {
    return request(`/songs/${songId}/play`, {
      method: 'POST'
    })
  }
}

// 收藏相关API
export const favoriteAPI = {
  // 获取收藏的歌曲
  getFavoriteSongs() {
    return request('/favorite/songs')
  },
  
  // 收藏歌曲
  addFavorite(songId) {
    return request(`/favorite/songs/${songId}`, {
      method: 'POST'
    })
  },
  
  // 取消收藏
  removeFavorite(songId) {
    return request(`/favorite/songs/${songId}`, {
      method: 'DELETE'
    })
  },
  
  // 检查是否已收藏
  checkFavorite(songId) {
    return request(`/favorite/songs/${songId}/check`)
  },
  
  // 批量检查是否已收藏
  checkFavoritesBatch(songIds) {
    return request('/favorite/songs/check-batch', {
      method: 'POST',
      body: JSON.stringify({ song_ids: songIds })
    })
  }
}

// 管理员相关API
export const adminAPI = {
  // 检查管理员权限
  checkAdmin() {
    return request('/admin/check')
  },
  
  // 上传歌曲
  uploadSong(formData) {
    const token = getToken()
    return fetch(`${API_BASE_URL}/admin/songs/upload`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    }).then(res => res.json())
  },
  
  // 更新歌曲
  updateSong(songId, songData) {
    return request(`/admin/songs/${songId}`, {
      method: 'PUT',
      body: JSON.stringify(songData)
    })
  },
  
  // 删除歌曲
  deleteSong(songId) {
    return request(`/admin/songs/${songId}`, {
      method: 'DELETE'
    })
  },
  
  // 获取所有歌曲（管理员）
  getAllSongs(page = 1, perPage = 20) {
    return request(`/admin/songs?page=${page}&per_page=${perPage}`)
  },
  
  // 获取统计信息
  getStats() {
    return request('/admin/stats')
  },
  
  // 歌手管理
  getAllSingers() {
    return request('/admin/singers')
  },
  
  createSinger(data) {
    return request('/admin/singers', {
      method: 'POST',
      body: JSON.stringify(data)
    })
  },
  
  updateSinger(id, data) {
    return request(`/admin/singers/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  },
  
  deleteSinger(id) {
    return request(`/admin/singers/${id}`, {
      method: 'DELETE'
    })
  },
  
  // 用户管理
  getAllUsers() {
    return request('/admin/users')
  },
  
  toggleUserAdmin(id, isAdmin) {
    return request(`/admin/users/${id}/admin`, {
      method: 'PUT',
      body: JSON.stringify({ is_admin: isAdmin })
    })
  },
  
  deleteUser(id) {
    return request(`/admin/users/${id}`, {
      method: 'DELETE'
    })
  },
  
  // 歌曲推荐管理
  toggleSongFeatured(songId, isFeatured) {
    return request(`/admin/songs/${songId}/featured`, {
      method: 'PUT',
      body: JSON.stringify({ is_featured: isFeatured })
    })
  },
  
  toggleSongNew(songId, isNew) {
    return request(`/admin/songs/${songId}/new`, {
      method: 'PUT',
      body: JSON.stringify({ is_new: isNew })
    })
  },
  
  toggleSongRecommended(songId, isRecommended) {
    return request(`/admin/songs/${songId}/recommended`, {
      method: 'PUT',
      body: JSON.stringify({ is_recommended: isRecommended })
    })
  }
}

// 播放历史相关API
export const historyAPI = {
  // 记录播放历史
  recordPlay(songId) {
    return request('/history/record', {
      method: 'POST',
      body: JSON.stringify({ song_id: songId })
    })
  },
  
  // 获取播放历史
  getHistory(page = 1, perPage = 20) {
    return request(`/history/list?page=${page}&per_page=${perPage}`)
  },
  
  // 获取最近播放
  getRecent(limit = 10) {
    return request(`/history/recent?limit=${limit}`)
  },
  
  // 清空播放历史
  clearHistory() {
    return request('/history/clear', {
      method: 'DELETE'
    })
  },
  
  // 删除单条历史
  deleteHistoryItem(songId) {
    return request(`/history/${songId}`, {
      method: 'DELETE'
    })
  }
}

// 歌手相关API
export const singerAPI = {
  // 获取歌手列表
  getSingers(params = {}) {
    const queryString = new URLSearchParams(params).toString()
    return request(`/singers/list${queryString ? '?' + queryString : ''}`)
  },
  
  // 获取歌手详情
  getSinger(singerId) {
    return request(`/singers/${singerId}`)
  },
  
  // 获取歌手的歌曲
  getSingerSongs(singerId, page = 1, perPage = 20) {
    return request(`/singers/${singerId}/songs?page=${page}&per_page=${perPage}`)
  },
  
  // 获取所有国家/地区
  getCountries() {
    return request('/singers/countries')
  },
  
  // 获取所有流派
  getGenres() {
    return request('/singers/genres')
  },
  
  // 获取歌曲的歌手列表
  getSongSingers(songId) {
    return request(`/singers/song/${songId}/singers`)
  },
  
  // ==================== 管理员API ====================
  
  // 创建歌手
  createSinger(singerData) {
    return request('/singers/create', {
      method: 'POST',
      body: JSON.stringify(singerData)
    })
  },
  
  // 更新歌手
  updateSinger(singerId, singerData) {
    return request(`/singers/${singerId}`, {
      method: 'PUT',
      body: JSON.stringify(singerData)
    })
  },
  
  // 删除歌手
  deleteSinger(singerId) {
    return request(`/singers/${singerId}`, {
      method: 'DELETE'
    })
  },
  
  // 上传歌手头像
  uploadAvatar(file) {
    const token = getToken()
    const formData = new FormData()
    formData.append('avatar', file)
    
    return fetch(`${API_BASE_URL}/singers/upload-avatar`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    }).then(res => res.json())
  },
  
  // 关联歌曲和歌手
  linkSongSinger(songId, singerId) {
    return request('/singers/link-song', {
      method: 'POST',
      body: JSON.stringify({ song_id: songId, singer_id: singerId })
    })
  },
  
  // 取消关联
  unlinkSongSinger(songId, singerId) {
    return request('/singers/unlink-song', {
      method: 'POST',
      body: JSON.stringify({ song_id: songId, singer_id: singerId })
    })
  }
}

// 排行榜相关API
export const rankingAPI = {
  // 获取排行榜
  getRanking(type = 'week', genre = 'all', limit = 50) {
    return request(`/ranking?type=${type}&genre=${genre}&limit=${limit}`)
  },
  
  // 获取音乐流派列表
  getGenres() {
    return request('/ranking/genres')
  },
  
  // 获取排行榜统计
  getStats() {
    return request('/ranking/stats')
  }
}

// 歌单相关API
export const playlistAPI = {
  // 创建歌单
  createPlaylist(playlistData) {
    return request('/playlist/create', {
      method: 'POST',
      body: JSON.stringify(playlistData)
    })
  },
  
  // 获取歌单详情
  getPlaylist(playlistId) {
    return request(`/playlist/${playlistId}`)
  },
  
  // 获取我的歌单
  getMyPlaylists() {
    return request('/playlist/my')
  },
  
  // 更新歌单
  updatePlaylist(playlistId, playlistData) {
    return request(`/playlist/${playlistId}`, {
      method: 'PUT',
      body: JSON.stringify(playlistData)
    })
  },
  
  // 删除歌单
  deletePlaylist(playlistId) {
    return request(`/playlist/${playlistId}`, {
      method: 'DELETE'
    })
  },
  
  // 添加歌曲到歌单
  addSongToPlaylist(playlistId, songId) {
    return request(`/playlist/${playlistId}/songs`, {
      method: 'POST',
      body: JSON.stringify({ song_id: songId })
    })
  },
  
  // 从歌单移除歌曲
  removeSongFromPlaylist(playlistId, songId) {
    return request(`/playlist/${playlistId}/songs/${songId}`, {
      method: 'DELETE'
    })
  },
  
  // ==================== 新增：公共歌单功能 ====================
  
  // 获取公共歌单
  getPublicPlaylists(params = {}) {
    const queryString = new URLSearchParams(params).toString()
    return request(`/playlist/public${queryString ? '?' + queryString : ''}`)
  },
  
  // 获取推荐歌单
  getFeaturedPlaylists(limit = 10) {
    return request(`/playlist/featured?limit=${limit}`)
  },
  
  // 增加播放次数
  incrementPlayCount(playlistId) {
    return request(`/playlist/${playlistId}/play`, {
      method: 'POST'
    })
  },
  
  // 更新歌单设置
  updateSettings(playlistId, settings) {
    return request(`/playlist/${playlistId}/settings`, {
      method: 'PUT',
      body: JSON.stringify(settings)
    })
  },
  
  // ==================== 收藏歌单功能 ====================
  
  // 收藏歌单
  collectPlaylist(playlistId) {
    return request(`/playlist/${playlistId}/collect`, {
      method: 'POST'
    })
  },
  
  // 取消收藏歌单
  uncollectPlaylist(playlistId) {
    return request(`/playlist/${playlistId}/collect`, {
      method: 'DELETE'
    })
  },
  
  // 检查歌单是否已收藏
  checkPlaylistCollected(playlistId) {
    return request(`/playlist/${playlistId}/is-collected`)
  },
  
  // 获取收藏的歌单
  getCollectedPlaylists() {
    return request('/playlist/collected')
  }
}
