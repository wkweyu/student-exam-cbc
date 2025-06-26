import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";

export default function Subjects() {
  const [subjects, setSubjects] = useState([]);

  useEffect(() => {
    api.get("subjects/").then((res) => setSubjects(res.data));
  }, []);

  const handleDelete = async (id) => {
    if (confirm("Delete this subject?")) {
      await api.delete(`subjects/${id}/`);
      setSubjects((prev) => prev.filter((s) => s.id !== id));
    }
  };

  return (
    <div className="p-4">
      <div className="flex justify-between mb-4">
        <h2 className="text-xl font-bold">Subjects</h2>
        <Link
          to="/subjects/new"
          className="bg-green-600 text-white px-4 py-2 rounded"
        >
          + Add Subject
        </Link>
      </div>
      <ul className="space-y-2">
        {subjects.map((s) => (
          <li
            key={s.id}
            className="border p-2 flex justify-between items-center"
          >
            <div>
              {s.name} - {s.stream_id?.class_id?.name} {s.stream_id?.name} (
              {s.teacher_id?.name})
            </div>
            <div className="space-x-2">
              <Link
                to={`/subjects/${s.id}`}
                className="text-blue-600 underline"
              >
                Edit
              </Link>
              <button
                onClick={() => handleDelete(s.id)}
                className="text-red-600"
              >
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
