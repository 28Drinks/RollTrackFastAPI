import React, { useEffect, useState } from "react";



const Inventory = () => {
    const [user, setUser] = useState();
    const [inventory, setInventory] = useState([]);
    const [newItem, setNewItem] = useState({});
    const token = localStorage.getItem("token");

    const [bot, setBot] = useState({
        bot_number: 0,
        bot: {
            name: "",
            number: 0,
            // image_url: "",
            // revealed: true,
            stats: {
            // sportshares: 0,
            freebet: 0,
            // comboboost: 0
            },
            traits: {
            sport: "",
            // background: "",
            // body: "",
            // eyes: "",
            // teeth: ""
            }
        },
        // claimed: true,
        // claimed_at: "",
        // value: 0,
        // buy_price: 0,
        // unlocks_in: ""
    });

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
                setInventory(userData.inventory);
                console.log(userData)
            }
        }
        getCurrentUser();
    }, []);
  
  
    if (!user) {
      console.log("User data not found"); // for debugging
      return <div>Not logged in</div>;
    }

    const handleChange = (e) => {
        const { name, value } = e.target;
        if (name === "bot_number") {
          setBot((prevState) => ({
            ...prevState,
            [name]: value
          }));
        } else if ( name === "sport" || name === "background" || name === "body" || name === "eyes" || name === "teeth") {
          setBot((prevState) => ({
            ...prevState,
            bot: {
              ...prevState.bot,
              traits: {
                ...prevState.bot.traits,
                [name]: value,
               },
              },
          }));
        } else {
          setBot((prevState) => ({
            ...prevState,
            bot: {
              ...prevState.bot,
              stats: {
                ...prevState.bot.stats,
                [name]: value,
              },
            },
          }));
        }
      };


      async function handleSubmit(e) {
        e.preventDefault();
        setBot({
          ...bot,
          bot_number: e.target.bot_number.value,
          bot: {
            ...bot.bot,
            name: e.target.name.value,
            number: e.target.number.value,
            // image_url: e.target.image_url.value,
            stats: {
              ...bot.bot.stats,
              // sportshares: e.target.sportshares.value,
              freebet: e.target.freebet.value,
              // comboboost: e.target.comboboost.value
            },
            traits: {
              ...bot.bot.traits,
              sport: e.target.sport.value,
              // background: e.target.background.value,
              // body: e.target.body.value,
              // eyes: e.target.eyes.value,
              // teeth: e.target.teeth.value
            }
          }
        });
        console.log(bot);
        const requestOptions = {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "token": token,
          },
          body: JSON.stringify(bot),
        };
        console.log(user.username)
        const response = await fetch("http://167.172.166.15:8000/api/user/" + user.username + "/inventory", requestOptions)
        if (response.ok) {
            console.log("Adding new item")
            setInventory(inventory => [...inventory, bot]);
        } else {
            console.error("Failed to update inventory")
        }
      };


    const handleDelete = async (botNumber) => {
        const token = localStorage.getItem("token");
        const requestOptions = {
            method: "DELETE",
            headers: { "token": token }
        }
        const response = await fetch(`http://167.172.166.15:8000/api/user/${user.username}/inventory/${botNumber}`, requestOptions);
        if (response.ok) {
            // Update the inventory list on the client-side after deletion
            setInventory(inventory.filter((item) => item.bot_number !== botNumber));
        } else {
            console.error(`Failed to delete item ${botNumber}`);
        }
    };


    // const values = Object.values(inventory);

    if (user.inventory) {

        const inventoryList = Array.isArray(inventory) ? inventory.map((item, index) => (
            <div key={index}>
                <ul>
                <br/>
                {Object.entries(item).map(([key, value]) => (
                    <li key={key}>{key}: {JSON.stringify(value)}</li>
                ))}
                <br/>
                </ul>
                <button onClick={() => handleDelete(item.bot_number)}>Delete</button>
            <br/>
            </div>
        )) : null;

    return (
        <>  
            <h2>Add inventoy entry:</h2>
            <div>
          <form onSubmit={handleSubmit}>
            <label>
              Bot_number:
              <input type="number" name="bot_number" placeholder={bot.bot_number} onChange={(e) => handleChange(e, setBot, bot.bot_number)}  />
            </label>
            <label>
              Name:
              <input type="text" name="name" placeholder="some name" onChange={(e) => handleChange(e, setBot, bot.bot.name)} />
            </label>
            <label>
              Number:
              <input type="number" name="number" placeholder={bot.bot.number}  onChange={(e) => handleChange(e, setBot, bot.bot.number)} />
            </label>
            {/* <label>
              Image URL:
              <input type="text" name="image_url"  onChange={(e) => handleChange(e, setBot, bot.bot.image_url)} />
            </label> */}
            {/* <label>
              Sport Shares:
              <input type="number" name="sportshares"  onChange={(e) => handleChange(e, setBot, bot.bot.stats.sportshares)}/>
            </label> */}
            <label>
              Free Bet:
              <input type="number" name="freebet" placeholder={bot.bot.stats.freebet}  onChange={(e) => handleChange(e, setBot, bot.bot.stats.freebet)} />
            </label>
            {/* <label>
              Combo Boost:
              <input type="number" name="comboboost"  onChange={(e) => handleChange(e, setBot, bot.bot.stats.comboboost)} />
            </label> */}
            <label>
              Sport:
              <input type="text" name="sport" placeholder="some sport" onChange={(e) => handleChange(e, setBot, bot.bot.traits.sport)}/>
            </label>
            {/* <label>
              Background:
              <input type="text" name="background" onChange={(e) => handleChange(e, setBot, bot.bot.traits.background)} />
            </label>
            <label>
              Body:
              <input type="text" name="body" onChange={(e) => handleChange(e, setBot, bot.bot.traits.body)} />
            </label>
            <label>
              Eyes:
              <input type="text" name="eyes" onChange={(e) => handleChange(e, setBot, bot.bot.traits.eyes)} />
            </label>
            <label>
              Teeth:
              <input type="text" name="teeth"  onChange={(e) => handleChange(e, setBot, bot.bot.traits.eyes)}/>
            </label> */}
            <label>
              <input type="submit" value="Submit" />
            </label>
            </form>
          </div>
          <br/>
            <h2>Inventory:</h2>
            {inventoryList}
        </>
    );
    } else {
        return <div>No items in inventory <br/>
        <div>
          <h2>Add a Bot to the Inventory:</h2>
          <form onSubmit={handleSubmit}>
            <label>
              Bot_number:
              <input type="number" name="bot_number" defaultValue={bot.bot_number} onChange={(e) => handleChange(e, setBot, bot.bot_number)}  />
            </label>
            <label>
              Name:
              <input type="text" name="name" onChange={(e) => handleChange(e, setBot, bot.bot.name)} />
            </label>
            <label>
              Number:
              <input type="number" name="number"  onChange={(e) => handleChange(e, setBot, bot.bot.number)} />
            </label>
            {/* <label>
              Image URL:
              <input type="text" name="image_url"  onChange={(e) => handleChange(e, setBot, bot.bot.image_url)} />
            </label> */}
            {/* <label>
              Sport Shares:
              <input type="number" name="sportshares"  onChange={(e) => handleChange(e, setBot, bot.bot.stats.sportshares)}/>
            </label> */}
            <label>
              Free Bet:
              <input type="number" name="freebet"  onChange={(e) => handleChange(e, setBot, bot.bot.stats.freebet)} />
            </label>
            {/* <label>
              Combo Boost:
              <input type="number" name="comboboost"  onChange={(e) => handleChange(e, setBot, bot.bot.stats.comboboost)} />
            </label> */}
            <label>
              Sport:
              <input type="text" name="sport"  onChange={(e) => handleChange(e, setBot, bot.bot.traits.sport)}/>
            </label>
            {/* <label>
              Background:
              <input type="text" name="background" onChange={(e) => handleChange(e, setBot, bot.bot.traits.background)} />
            </label>
            <label>
              Body:
              <input type="text" name="body" onChange={(e) => handleChange(e, setBot, bot.bot.traits.body)} />
            </label>
            <label>
              Eyes:
              <input type="text" name="eyes" onChange={(e) => handleChange(e, setBot, bot.bot.traits.eyes)} />
            </label>
            <label>
              Teeth:
              <input type="text" name="teeth"  onChange={(e) => handleChange(e, setBot, bot.bot.traits.eyes)}/>
            </label> */}
            <label>
              <input type="submit" value="Submit" />
            </label>
            </form>
          </div></div>
    }
};


export default Inventory;