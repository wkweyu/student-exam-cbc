import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../api/axios";
import toast from "react-hot-toast";

export default function TeacherForm() {
  const [formData, setFormData] = useState({ name: "" });
  const { id } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    if (id) api.get(`teachers/${id}/`).then((res) => setFormData(res.data));
  }, [id]);

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.name) return toast.error("Name is required");

    try {
      if (id) {
        await api.put(`teachers/${id}/`, formData);
        toast.success("Teacher updated");
      } else {
        await api.post("teachers/", formData);
        toast.success("Teacher created");
      }
      navigate("/teachers");
    } catch (err) {
      toast.error("Failed to save");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10">
      <h2 className="text-xl font-bold mb-4">{id ? "Edit" : "Add"} Teacher</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          name="name"
          className="border p-2 w-full"
          placeholder="Teacher Name"
          value={formData.name}
          onChange={handleChange}
        />
        <button className="bg-blue-600 text-white px-4 py-2">
          {id ? "Update" : "Create"}
        </button>
      </form>
    </div>
  );
}
