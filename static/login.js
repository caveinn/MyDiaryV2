buton = document.getElementById('loginbtn')
document.getElementById("loginform").addEventListener("submit", function(e) {
e.preventDefault(); });


buton.onclick = function(){
  
  let user= {
  username: document.getElementById("username").value,
  password: document.getElementById("password").value,
  }

	fetch("/api/v2/auth/login", {
        method: 'POST',
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(user)
      })
      .then(res => res.json())

      .then(data => {
        document.getElementById("message").innerHTML = data.message;
        console.log(data)
        if (data.message === "Your account was created") {
          let msg = data.message;
          document.getElementById("message").innerHTML = msg;
          window.location.href = "/login";
        } else {
          let msg = Object.values(data);
          console.log(msg)
          document.getElementById("message").innerHTML = msg;
          setTimeout(() => {document.getElementById("message").innerHTML = "";}, 5000);

        }

      })
      // catch error that may occur
      .catch(error => console.log(error));

}