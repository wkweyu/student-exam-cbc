import { useEffect, useState } from "react";
import api from "../api/axios";
import { useNavigate, useParams } from "react-router-dom";

export default function StreamForm() {
  const [formData, setFormData] = useState({ name: "", class_id: "" });
  const [classes, setClasses] = useState([]);
  const navigate = useNavigate();
  const { id } = useParams();

  useEffect(() => {
    api.get("classes/").then((res) => setClasses(res.data));

    if (id) {
      api.get(`streams/${id}/`).then((res) => setFormData(res.data));
    }
  }, [id]);

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (id) {
      await api.put(`streams/${id}/`, formData);
    } else {
      await api.post("streams/", formData);
    }
    navigate("/streams");
  };

  return (
    <div className="max-w-md mx-auto mt-10">
      <h2 className="text-xl font-bold mb-4">{id ? "Edit" : "Add"} Stream</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          name="name"
          placeholder="Stream Name (e.g., East, West)"
          className="border p-2 w-full"
          value={formData.name}
          onChange={handleChange}
        />
        <select
          name="class_id"
          className="border p-2 w-full"
          value={formData.class_id}
          onChange={handleChange}
        >
          <option value="">Select Class</option>
          {classes.map((cls) => (
            <option key={cls.id} value={cls.id}>
              {cls.name} ({cls.academic_year})
            </option>
          ))}
        </select>
        <select
          name="stream_id"
          className="border p-2 w-full"
          value={formData.stream_id}
          onChange={handleChange}
        >
          <option value="">Select Stream</option>
          {streams.map((stream) => (
            <option key={stream.id} value={stream.id}>
              {stream.class_id?.name} - {stream.name}
            </option>
          ))}
        </select>

        <button className="bg-blue-600 text-white px-4 py-2">
          {id ? "Update" : "Create"}
        </button>
      </form>
    </div>
  );
}
