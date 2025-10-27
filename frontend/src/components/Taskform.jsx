import { useState } from 'react'


export default function TaskForm({ onAdd }) {
    const [title, setTitle] = useState('')
    const [duration, setDuration] = useState('30')
    const [due, setDue] = useState('')


    const submit = async (e) => {
    e.preventDefault()
    const payload = {
        title,
        duration_min: duration ? parseInt(duration) : null,
        due: due || null,
    }
    await onAdd(payload)
    setTitle(''); setDuration('30'); setDue('')
    }


    return (
        <form onSubmit={submit} className="flex gap-2 items-end">
            <div className="flex-1">
                <label className="block text-sm mb-1">Task</label>
                <input className="input w-full" value={title} onChange={e=>setTitle(e.target.value)} placeholder="Write spec, standup, etc" required />
            </div>
            <div>
                <label className="block text-sm mb-1">Duration (min)</label>
                <input className="input w-28" type="number" min="5" value={duration} onChange={e=>setDuration(e.target.value)} />
            </div>
            <div>
                <label className="block text-sm mb-1">Due (ISO)</label>
                <input className="input w-56" type="datetime-local" value={due} onChange={e=>setDue(e.target.value)} />
                </div>
            <button className="btn">Add</button>
        </form>
    )
}