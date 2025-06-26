import { useEffect, useState } from "react";
import api from "../api/axios";
import toast from "react-hot-toast";

export default function ResultsEntry() {
  const [filters, setFilters] = useState({
    year: "",
    term: "",
    exam: "",
    class_id: "",
    stream_id: "",
    subject_id: "",
  });

  const [options, setOptions] = useState({
    years: [],
    terms: [],
    exams: [],
    classes: [],
    streams: [],
    subjects: [],
  });

  const [students, setStudents] = useState([]);
  const [scores, setScores] = useState({});

  useEffect(() => {
    async function fetchDropdowns() {
      const [years, terms, exams, classes, streams, subjects] =
        await Promise.all([
          api.get("/academic-years/"),
          api.get("/terms/"),
          api.get("/exams/"),
          api.get("/classes/"),
          api.get("/streams/"),
          api.get("/subjects/"),
        ]);
      setOptions({
        years: years.data,
        terms: terms.data,
        exams: exams.data,
        classes: classes.data,
        streams: streams.data,
        subjects: subjects.data,
      });
    }

    fetchDropdowns();
  }, []);

  useEffect(() => {
    const { class_id, stream_id } = filters;
    if (class_id && stream_id) {
      api
        .get(`/students/?class_id=${class_id}&stream_id=${stream_id}`)
        .then((res) => {
          setStudents(res.data);
          const initialScores = {};
          res.data.forEach((s) => (initialScores[s.id] = ""));
          setScores(initialScores);
        });
    }
  }, [filters.class_id, filters.stream_id]);

  const handleChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  const handleScoreChange = (studentId, value) => {
    setScores({ ...scores, [studentId]: value });
  };

  const handleSubmit = async () => {
    const { exam, subject_id } = filters;
    if (!exam || !subject_id)
      return toast.error("Please select exam and subject");

    const payload = {
      exam_id: exam,
      subject_id: subject_id,
      results: Object.entries(scores).map(([student_id, marks]) => ({
        student_id,
        marks: parseFloat(marks),
      })),
    };

    try {
      await api.post("/results/bulk/", payload);
      toast.success("Results saved successfully");
    } catch (err) {
      toast.error("Failed to save results");
    }
  };

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Enter Exam Results</h1>

      {/* FILTER FORM */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
        <select
          name="year"
          value={filters.year}
          onChange={handleChange}
          className="border p-2 rounded"
        >
          <option value="">Select Year</option>
          {options.years.map((y) => (
            <option key={y.id} value={y.id}>
              {y.year}
            </option>
          ))}
        </select>

        <select
          name="term"
          value={filters.term}
          onChange={handleChange}
          className="border p-2 rounded"
        >
          <option value="">Select Term</option>
          {options.terms.map((t) => (
            <option key={t.id} value={t.id}>
              {t.name}
            </option>
          ))}
        </select>

        <select
          name="exam"
          value={filters.exam}
          onChange={handleChange}
          className="border p-2 rounded"
        >
          <option value="">Select Exam</option>
          {options.exams.map((e) => (
            <option key={e.id} value={e.id}>
              {e.name}
            </option>
          ))}
        </select>

        <select
          name="subject_id"
          value={filters.subject_id}
          onChange={handleChange}
          className="border p-2 rounded"
        >
          <option value="">Select Subject</option>
          {options.subjects.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name}
            </option>
          ))}
        </select>

        <select
          name="class_id"
          value={filters.class_id}
          onChange={handleChange}
          className="border p-2 rounded"
        >
          <option value="">Select Class</option>
          {options.classes.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>

        <select
          name="stream_id"
          value={filters.stream_id}
          onChange={handleChange}
          className="border p-2 rounded"
        >
          <option value="">Select Stream</option>
          {options.streams.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name}
            </option>
          ))}
        </select>
      </div>

      {/* RESULTS ENTRY TABLE */}
      {students.length > 0 && (
        <>
          <table className="w-full border mb-4">
            <thead>
              <tr className="bg-gray-100">
                <th className="border p-2 text-left">Student</th>
                <th className="border p-2">Score</th>
              </tr>
            </thead>
            <tbody>
              {students.map((s) => (
                <tr key={s.id}>
                  <td className="border p-2">{s.name}</td>
                  <td className="border p-2">
                    <input
                      type="number"
                      step="0.1"
                      className="border p-1 w-full"
                      value={scores[s.id] || ""}
                      onChange={(e) => handleScoreChange(s.id, e.target.value)}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <button
            onClick={handleSubmit}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Save Results
          </button>
        </>
      )}
    </div>
  );
}
