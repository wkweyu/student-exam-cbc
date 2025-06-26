import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./auth/Login";
import Dashboard from "./pages/Dashboard";
import Students from "./pages/Students";
import ProtectedRoute from "./components/ProtectedRoute";
import StudentForm from "./pages/StudentForm";
import ClassForm from "./pages/ClassForm";
import StreamForm from "./pages/StreamForm";
import Teachers from "./pages/Teachers";
import TeacherForm from "./pages/TeacherForm";
import Subjects from "./pages/Subjects";
import SubjectForm from "./pages/SubjectForm";
import Exams from "./pages/Exams";
import ExamForm from "./pages/ExamForm";
import ResultsEntry from "./pages/ResultsEntry";

function App() {
  return (
    <Routes>
      <Route path="/students/new" element={<StudentForm />} />
      <Route path="/students/:id" element={<StudentForm />} />
      <Route path="/classes/new" element={<ClassForm />} />
      <Route path="/classes/:id" element={<ClassForm />} />
      <Route path="/streams/new" element={<StreamForm />} />
      <Route path="/streams/:id" element={<StreamForm />} />
      <Route path="/login" element={<Login />} />
      <Route element={<ProtectedRoute />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/students" element={<Students />} />
      </Route>
      <Route path="/teachers" element={<Teachers />} />
      <Route path="/teachers/new" element={<TeacherForm />} />
      <Route path="/teachers/:id" element={<TeacherForm />} />
      <Route path="/subjects" element={<Subjects />} />
      <Route path="/subjects/new" element={<SubjectForm />} />
      <Route path="/subjects/:id" element={<SubjectForm />} />
      <Route path="/exams" element={<Exams />} />
      <Route path="/exams/new" element={<ExamForm />} />
      <Route path="/exams/:id" element={<ExamForm />} />
      <Route path="/results-entry" element={<ResultsEntry />} />;
    </Routes>
  );
}

export default App;
