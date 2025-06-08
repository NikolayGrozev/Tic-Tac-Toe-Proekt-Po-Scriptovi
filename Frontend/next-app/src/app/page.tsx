'use client'
import { useEffect, useState } from "react";
import { user } from "../(interfaces)/interfaces";

export default function Home() {
  const [users, setUsers] = useState<user[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/users/')
      .then((res) => {
        if (!res.ok) throw new Error('Failed to fetch');
        return res.json();
      })
      .then((data) => {
        setUsers(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);



  return (
    <div>
      <main>

        {
          (loading) ? <p> Loading...</p> : (error) ? <p> Error </p> : users.map((user, index) => {
            return(
            <ul key={index}>
              <p>
                id: {user.id}
              </p>
              <p key={index}>
                name: {user.username}
              </p>
              <p>
                email: {user.email}
              </p>
            </ul>
            );
          })
        }
        
      </main>
    </div>
  );
}
