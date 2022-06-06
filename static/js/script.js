window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

let deleteBtn = document.getElementById("delete-venue");

deleteBtn.addEventListener("click", async (e) => {
  let venueId = e.target.dataset["id"];

  try {
    await fetch(`/venues/${venueId}/delete`, {
      method: "DELETE",
    });
    window.location.replace("/");
  } catch (error) {
    console.log(error);
  }
});
