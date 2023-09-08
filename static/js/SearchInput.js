const searchInput = document.getElementById("search_input");
const container = document.getElementById("search_container");

searchInput.addEventListener("change", () => {
    for (let i = 0; i < container.children.length; i++) {
        let item = container.children[i];
        let header = item.querySelector(".search-item-name");

        if (header.innerHTML.toLowerCase().indexOf(searchInput.value.toLowerCase()) === -1) {
            item.setAttribute("hidden", "");
        } else {
            if (item.hasAttribute("hidden")) {
                item.removeAttribute("hidden");
            }
        }
    }
})