import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";

export default function Classes() {
  const [classes, setClasses] = useState([]);

  useEffect(() => {
    fetchClasses();
  }, []);

  const fetchClasses = async () => {
    const res = await api.get("classes/");
    setClasses(res.data);
  };

  const handleDelete = async (id) => {
    if (confirm("Delete this class?")) {
      await api.delete(`classes/${id}/`);
      fetchClasses();
    }
  };

  return (
    <div className="p-4">
      <div className="flex justify-between mb-4">
        <h2 className="text-xl font-bold">Classes</h2>
        <Link
          to="/classes/new"
          className="bg-green-600 text-white px-4 py-2 rounded"
        >
          + Add Class
        </Link>
      </div>
      <ul className="space-y-2">
        {classes.map((cls) => (
          <li
            key={cls.id}
            className="border rounded p-2 flex justify-between items-center"
          >
            <div>
              {cls.name} ({cls.academic_year})
            </div>
            <div className="space-x-2">
              <Link
                to={`/classes/${cls.id}`}
                className="text-blue-600 underline"
              >
                Edit
              </Link>
              <button
                onClick={() => handleDelete(cls.id)}
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
