export default function TaskList({ tasks, onToggle, onDelete }) {
    return (
        <div className="card">
        <h3 className="text-lg font-semibold mb-3">Tasks</h3>
        <ul className="space-y-2">
            {tasks.map(t => (
                <li key={t.id} className="flex items-center justify-between p-2 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-800">
                    <label className="flex items-center gap-3">
                        <input type="checkbox" checked={t.is_done} onChange={()=>onToggle(t)} />
                        <span className={t.is_done ? 'line-through opacity-60' : ''}>{t.title}</span>
                    </label>
                    <div className="text-xs opacity-70 flex gap-3">
                        {t.duration_min ? <span>{t.duration_min}m</span> : null}
                        {t.due ? <span>{new Date(t.due).toLocaleString()}</span> : null}
                        <button onClick={()=>onDelete(t)} className="text-red-500">Delete</button>
                    </div>
                </li>
            ))}
        </ul>
    </div>
    )
}