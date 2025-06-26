import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";

export default function Exams() {
  const [exams, setExams] = useState([]);

  useEffect(() => {
    api.get("exams/").then((res) => setExams(res.data));
  }, []);

  const handleDelete = async (id) => {
    if (confirm("Delete this exam?")) {
      await api.delete(`exams/${id}/`);
      setExams(exams.filter((e) => e.id !== id));
    }
  };

  return (
    <div className="p-4">
      <div className="flex justify-between mb-4">
        <h2 className="text-xl font-bold">Exams</h2>
        <Link
          to="/exams/new"
          className="bg-green-600 text-white px-4 py-2 rounded"
        >
          + Add Exam
        </Link>
      </div>
      <ul className="space-y-2">
        {exams.map((e) => (
          <li
            key={e.id}
            className="border p-2 flex justify-between items-center"
          >
            <div>
              {e.name} — {e.term.name} ({e.term.academic_year.year}) | Weight:{" "}
              {e.weight}
            </div>
            <div className="space-x-2">
              <Link to={`/exams/${e.id}`} className="text-blue-600 underline">
                Edit
              </Link>
              <button
                onClick={() => handleDelete(e.id)}
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
