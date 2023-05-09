import React, { useState, useEffect } from 'react';

const Profile = () => {

  const [user, setUser] = useState();

  useEffect( () => {
      async function getCurrentUser() {
          const token = localStorage.getItem("token");
          const requestOptions = {
              method: "GET",
              headers: {"token": token}
          }

          const response = await fetch('http://167.172.166.15:8000/api/users/me', requestOptions);
          if (response.ok) {
              const userData = await response.json();
              setUser(userData);
          }
      }
      getCurrentUser();
  }, []);


  if (!user) {
    console.log("User data not found"); // for debugging
    return <div>Not logged in</div>;
  }

  console.log(user)

  return (
    <div>
      <h2>Welcome, {user.username}!</h2>
      <p>Email: {user.email}</p>
    </div>
  );
};


export default Profile