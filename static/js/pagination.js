function pagination_load(page_count, active_page_number) {
    const pagination_line_length = 10
    const pageList = document.getElementById("page_list")
    active_page_number = Number(active_page_number)

    function add_page_number(page_number) {
        let new_list_item = document.createElement("li");
        new_list_item.className = "page-item"
        let new_link = document.createElement("a")
        new_link.className = "page-link"
        new_link.textContent = page_number

        if (page_number == "...") {
            new_link.href = "" 
            new_link.textContent = "..."
        } else {
            new_link.href = "?page=" + page_number

            if (page_number == active_page_number) {
                new_list_item.className += " active"
            }
        }

        new_list_item.appendChild(new_link)
        pageList.appendChild(new_list_item)
    }

    if (page_count <= pagination_line_length) {
        for (let page_number = 1; page_number <= page_count; page_number++) {
            add_page_number(page_number)
        }
    } else {
        if (active_page_number == page_count) {
            add_page_number(1)
            add_page_number("...")

            for (let page_number = active_page_number - pagination_line_length; page_number <= page_count; page_number++) {
                add_page_number(page_number)
            }
        } else if (page_count - active_page_number <= pagination_line_length) {
            add_page_number(1)
            add_page_number("...")

            for (let page_number = page_count - pagination_line_length; page_number <= page_count; page_number++) {
                add_page_number(page_number)
            }
        } else if (pagination_line_length > active_page_number) {
            for (let page_number = 1; page_number <= pagination_line_length - 1; page_number++) {
                add_page_number(page_number)
            }

            add_page_number("...")
            add_page_number(page_count)
        } else {
            add_page_number(1)
            add_page_number("...")

            for (let page_number = active_page_number; page_number <= active_page_number + pagination_line_length - 1; page_number++) {
                add_page_number(page_number)
            }

            add_page_number("...")
            add_page_number(page_count)
        }
    }
}