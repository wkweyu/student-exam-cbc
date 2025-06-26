import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../api/axios";
import toast from "react-hot-toast";

export default function SubjectForm() {
  const [formData, setFormData] = useState({
    name: "",
    stream_id: "",
    teacher_id: "",
  });
  const [streams, setStreams] = useState([]);
  const [teachers, setTeachers] = useState([]);
  const navigate = useNavigate();
  const { id } = useParams();

  useEffect(() => {
    api.get("streams/").then((res) => setStreams(res.data));
    api.get("teachers/").then((res) => setTeachers(res.data));
    if (id) api.get(`subjects/${id}/`).then((res) => setFormData(res.data));
  }, [id]);

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    const { name, stream_id, teacher_id } = formData;
    if (!name || !stream_id || !teacher_id)
      return toast.error("All fields required");

    try {
      if (id) {
        await api.put(`subjects/${id}/`, formData);
        toast.success("Subject updated");
      } else {
        await api.post("subjects/", formData);
        toast.success("Subject created");
      }
      navigate("/subjects");
    } catch {
      toast.error("Error saving subject");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10">
      <h2 className="text-xl font-bold mb-4">{id ? "Edit" : "Add"} Subject</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          name="name"
          className="border p-2 w-full"
          placeholder="Subject Name"
          value={formData.name}
          onChange={handleChange}
        />
        <select
          name="stream_id"
          className="border p-2 w-full"
          value={formData.stream_id}
          onChange={handleChange}
        >
          <option value="">Select Stream</option>
          {streams.map((s) => (
            <option key={s.id} value={s.id}>
              {s.class_id?.name} - {s.name}
            </option>
          ))}
        </select>
        <select
          name="teacher_id"
          className="border p-2 w-full"
          value={formData.teacher_id}
          onChange={handleChange}
        >
          <option value="">Select Teacher</option>
          {teachers.map((t) => (
            <option key={t.id} value={t.id}>
              {t.name}
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
