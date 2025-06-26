import { useEffect, useState } from "react";
import api from "../api/axios";
import { useNavigate, useParams } from "react-router-dom";

export default function ClassForm() {
  const [formData, setFormData] = useState({ name: "", academic_year: "" });
  const navigate = useNavigate();
  const { id } = useParams(); // edit mode

  useEffect(() => {
    if (id) {
      api.get(`classes/${id}/`).then((res) => setFormData(res.data));
    }
  }, [id]);

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (id) {
      await api.put(`classes/${id}/`, formData);
    } else {
      await api.post("classes/", formData);
    }
    navigate("/classes");
  };

  return (
    <div className="max-w-md mx-auto mt-10">
      <h2 className="text-xl font-bold mb-4">{id ? "Edit" : "Add"} Class</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          name="name"
          placeholder="Class Name (e.g., Grade 5)"
          className="border p-2 w-full"
          value={formData.name}
          onChange={handleChange}
        />
        <input
          name="academic_year"
          placeholder="Academic Year (e.g., 2025)"
          className="border p-2 w-full"
          value={formData.academic_year}
          onChange={handleChange}
        />
        <button className="bg-blue-600 text-white px-4 py-2">
          {id ? "Update" : "Create"}
        </button>
      </form>
    </div>
  );
}
