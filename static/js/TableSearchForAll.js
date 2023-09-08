const table = document.getElementById("mytable");
const searchItems = document.querySelectorAll(".search-table-item");
const searchedFields = document.getElementById("searched-fields");

searchItems.forEach((e) => e.addEventListener("change", () => {
    sortTable();
}))

function sortTable() {
    for (let i = 0; i < searchedFields.children.length; i++) {
        let entry = searchedFields.children[i];
        let tds = entry.querySelectorAll(".sorted-field")
        for (let k = 0; k < searchItems.length; k++) {
            let query = searchItems[k];
            let td = tds[k];

            if (td.innerHTML.toLowerCase().indexOf(query.children[0].value.toLowerCase()) === -1) {
                td.parentNode.setAttribute("hidden", "");
                break;
            } else {
                if (td.parentNode.hasAttribute("hidden")) {
                    td.parentNode.removeAttribute("hidden");
                }
            }
        }
    }
}

