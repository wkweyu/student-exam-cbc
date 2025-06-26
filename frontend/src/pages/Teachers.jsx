import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";

export default function Teachers() {
  const [teachers, setTeachers] = useState([]);

  useEffect(() => {
    api.get("teachers/").then((res) => setTeachers(res.data));
  }, []);

  const handleDelete = async (id) => {
    if (confirm("Delete this teacher?")) {
      await api.delete(`teachers/${id}/`);
      setTeachers((prev) => prev.filter((t) => t.id !== id));
    }
  };

  return (
    <div className="p-4">
      <div className="flex justify-between mb-4">
        <h2 className="text-xl font-bold">Teachers</h2>
        <Link
          to="/teachers/new"
          className="bg-green-600 text-white px-4 py-2 rounded"
        >
          + Add Teacher
        </Link>
      </div>
      <ul className="space-y-2">
        {teachers.map((t) => (
          <li
            key={t.id}
            className="border p-2 flex justify-between items-center"
          >
            <div>{t.name}</div>
            <div className="space-x-2">
              <Link
                to={`/teachers/${t.id}`}
                className="text-blue-600 underline"
              >
                Edit
              </Link>
              <button
                onClick={() => handleDelete(t.id)}
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
