import React, { createContext, useEffect, useState } from "react";

export const UserContext = createContext(null);

const User = ({ children }) => {
    
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
                console.log("userData:", userData); // for debugging
                setUser(userData);
            }
        }
        getCurrentUser();
    }, []);


    if (!user) {
        return  <div>Not logged in</div>;
    }

    return <UserContext.Provider value={user}>{children}</UserContext.Provider>;
};


export default User;