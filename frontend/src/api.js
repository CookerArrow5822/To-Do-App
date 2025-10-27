const BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5001'


export const api = {
    listTasks: () => fetch(`${BASE}/api/tasks`).then(r => r.json()),
    createTask: (data) => fetch(`${BASE}/api/tasks`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data)}).then(r => r.json()),
    updateTask: (id, data) => fetch(`${BASE}/api/tasks/${id}`, { method:'PUT', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data)}).then(r => r.json()),
    deleteTask: (id) => fetch(`${BASE}/api/tasks/${id}`, { method:'DELETE' }),
    suggest: () => fetch(`${BASE}/api/ai/suggest`, { method:'POST' }).then(r => r.json()),
}