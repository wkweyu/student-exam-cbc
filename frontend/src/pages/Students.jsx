// src/pages/StudentForm.jsx
import React, { useState, useEffect } from "react";
import axios from "../api/axios";
import { useNavigate, useParams } from "react-router-dom";
import toast from "react-hot-toast";

const StudentForm = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEditMode = Boolean(id);

  const [formData, setFormData] = useState({
    admission_number: "",
    first_name: "",
    middle_name: "",
    last_name: "",
    date_of_birth: "",
    gender: "M",
    photo: null,
    class_ref: "",
    stream: "",
    guardian_name: "",
    guardian_contact: "",
    guardian_email: "",
    address: "",
    emergency_contact: "",
  });

  const [classes, setClasses] = useState([]);
  const [streams, setStreams] = useState([]);

  useEffect(() => {
    axios.get("/api/students/classes/").then((res) => setClasses(res.data));
    axios.get("/api/students/streams/").then((res) => setStreams(res.data));

    if (isEditMode) {
      axios.get(`/api/students/${id}/`).then((res) => {
        const data = res.data;
        setFormData({ ...data, photo: null }); // Avoid setting image directly
      });
    }
  }, [id]);

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    if (files) {
      setFormData({ ...formData, [name]: files[0] });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const form = new FormData();
    Object.entries(formData).forEach(([key, value]) => {
      if (value !== null) form.append(key, value);
    });

    try {
      if (isEditMode) {
        await axios.put(`/api/students/${id}/`, form);
        toast.success("Student updated successfully");
      } else {
        await axios.post("/api/students/register/", form);
        toast.success("Student registered successfully");
      }
      navigate("/students");
    } catch (error) {
      toast.error("Error saving student. Check your input.");
      console.error(error);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white shadow rounded-lg mt-6">
      <h2 className="text-2xl font-semibold mb-4">
        {isEditMode ? "Edit Student" : "Register Student"}
      </h2>
      <form
        onSubmit={handleSubmit}
        className="grid grid-cols-1 md:grid-cols-2 gap-4"
        encType="multipart/form-data"
      >
        <input
          type="text"
          name="first_name"
          placeholder="First Name"
          value={formData.first_name}
          onChange={handleChange}
          required
          className="input"
        />
        <input
          type="text"
          name="middle_name"
          placeholder="Middle Name"
          value={formData.middle_name}
          onChange={handleChange}
          className="input"
        />
        <input
          type="text"
          name="last_name"
          placeholder="Last Name"
          value={formData.last_name}
          onChange={handleChange}
          required
          className="input"
        />
        <input
          type="date"
          name="date_of_birth"
          value={formData.date_of_birth}
          onChange={handleChange}
          required
          className="input"
        />

        <select
          name="gender"
          value={formData.gender}
          onChange={handleChange}
          className="input"
        >
          <option value="M">Male</option>
          <option value="F">Female</option>
          <option value="O">Other</option>
          <option value="U">Undisclosed</option>
        </select>

        <input
          type="file"
          name="photo"
          accept="image/*"
          onChange={handleChange}
          className="input"
        />

        <select
          name="class_ref"
          value={formData.class_ref}
          onChange={handleChange}
          required
          className="input"
        >
          <option value="">Select Class</option>
          {classes.map((cls) => (
            <option key={cls.id} value={cls.id}>
              {cls.grade_level} - {cls.year}
            </option>
          ))}
        </select>

        <select
          name="stream"
          value={formData.stream}
          onChange={handleChange}
          required
          className="input"
        >
          <option value="">Select Stream</option>
          {streams
            .filter(
              (stream) => stream.class_ref === parseInt(formData.class_ref)
            )
            .map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
        </select>

        <input
          type="text"
          name="guardian_name"
          placeholder="Guardian Name"
          value={formData.guardian_name}
          onChange={handleChange}
          className="input"
        />
        <input
          type="tel"
          name="guardian_contact"
          placeholder="Mobile Contact (e.g. 07XXXXXXXX)"
          pattern="^07\d{8}$"
          value={formData.guardian_contact}
          onChange={handleChange}
          className="input"
        />
        <input
          type="email"
          name="guardian_email"
          placeholder="Guardian Email"
          value={formData.guardian_email}
          onChange={handleChange}
          className="input"
        />
        <input
          type="text"
          name="emergency_contact"
          placeholder="Emergency Contact"
          value={formData.emergency_contact}
          onChange={handleChange}
          className="input"
        />
        <textarea
          name="address"
          placeholder="Address"
          value={formData.address}
          onChange={handleChange}
          className="input col-span-2"
        />

        <button
          type="submit"
          className="col-span-2 mt-4 bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
        >
          {isEditMode ? "Update Student" : "Register Student"}
        </button>
      </form>
    </div>
  );
};

export default StudentForm;
