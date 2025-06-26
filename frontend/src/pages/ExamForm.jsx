import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../api/axios";
import toast from "react-hot-toast";

export default function ExamForm() {
  const [formData, setFormData] = useState({
    name: "",
    term_id: "",
    weight: 1.0,
  });
  const [terms, setTerms] = useState([]);
  const { id } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    api.get("terms/").then((res) => setTerms(res.data));
    if (id) api.get(`exams/${id}/`).then((res) => setFormData(res.data));
  }, [id]);

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.name || !formData.term_id) {
      return toast.error("All fields required");
    }

    try {
      if (id) {
        await api.put(`exams/${id}/`, formData);
        toast.success("Exam updated");
      } else {
        await api.post("exams/", formData);
        toast.success("Exam created");
      }
      navigate("/exams");
    } catch {
      toast.error("Error saving exam");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10">
      <h2 className="text-xl font-bold mb-4">{id ? "Edit" : "Add"} Exam</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          name="name"
          placeholder="Exam Name"
          value={formData.name}
          onChange={handleChange}
          className="border p-2 w-full"
        />
        <select
          name="term_id"
          value={formData.term_id}
          onChange={handleChange}
          className="border p-2 w-full"
        >
          <option value="">Select Term</option>
          {terms.map((t) => (
            <option key={t.id} value={t.id}>
              {t.name} - {t.academic_year.year}
            </option>
          ))}
        </select>
        <input
          name="weight"
          type="number"
          step="0.1"
          value={formData.weight}
          onChange={handleChange}
          className="border p-2 w-full"
          placeholder="Weight (e.g. 0.3)"
        />
        <button className="bg-blue-600 text-white px-4 py-2">
          {id ? "Update" : "Create"}
        </button>
      </form>
    </div>
  );
}
