import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";

export default function Streams() {
  const [streams, setStreams] = useState([]);

  useEffect(() => {
    fetchStreams();
  }, []);

  const fetchStreams = async () => {
    const res = await api.get("streams/");
    setStreams(res.data);
  };

  const handleDelete = async (id) => {
    if (confirm("Delete this stream?")) {
      await api.delete(`streams/${id}/`);
      fetchStreams();
    }
  };

  return (
    <div className="p-4">
      <div className="flex justify-between mb-4">
        <h2 className="text-xl font-bold">Streams</h2>
        <Link
          to="/streams/new"
          className="bg-green-600 text-white px-4 py-2 rounded"
        >
          + Add Stream
        </Link>
      </div>
      <ul className="space-y-2">
        {streams.map((stream) => (
          <li
            key={stream.id}
            className="border rounded p-2 flex justify-between items-center"
          >
            <div>
              {stream.name} - {stream.class_id?.name} (
              {stream.class_id?.academic_year})
            </div>
            <div className="space-x-2">
              <Link
                to={`/streams/${stream.id}`}
                className="text-blue-600 underline"
              >
                Edit
              </Link>
              <button
                onClick={() => handleDelete(stream.id)}
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
