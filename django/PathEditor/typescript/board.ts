
let table: HTMLTableElement | null = null;
let row_count: number = 0;
let col_count: number = 0

document.addEventListener("DOMContentLoaded", () => {
    table = document.getElementById("board-table") as HTMLTableElement;
    if (!table) {
        console.error("table not found");
    }

    let selected_color_name = document.getElementById("selected-color-name");
    let selected_color_block = document.getElementById("selected-color-block");
    let current_color: string | null = null;

    let color_usage = new Map<String, number>;
    let unfinished_colors = 0;

    function setColorSwitcher(child: Element) {
        const colorBlock = child.children[0];
        const color = window.getComputedStyle(colorBlock).backgroundColor;
        color_usage.set(color, 0);
        console.log(color);
        child.addEventListener("click", () => {
            console.log("Color: " + color);
            console.log("Current color: " + current_color);

            if (current_color == color) {
                current_color = null;
                selected_color_name.textContent = "none";
                selected_color_block.style.backgroundColor = null;
                return
            }

            current_color = color;
            console.log("Switched to: " + current_color);
            selected_color_name.textContent = child.children[1].textContent;
            selected_color_block.style.backgroundColor = color;
        })
    }


    console.log("starting");
    const color_selector = document.getElementById("color-selector");
    if (!color_selector) {
        console.error("color selector not found");
    }

    for (const child of color_selector.children) {
        setColorSwitcher(child);
    }


    const container = document.getElementById("board-container");
    if (!container) {
        console.error("container not found");
    }


    row_count = parseInt(document.getElementById("rows").textContent)
    col_count = parseInt(document.getElementById("cols").textContent)

    function getMarker(color: string) {
        let marker = document.createElement("div");
        marker.style.transform = "translate(-50%, -50%)";
        marker.style.borderRadius = "50%";
        marker.style.backgroundColor = color;
        marker.style.width = "50%";
        marker.style.height = "50%";
        marker.style.position = "relative";
        marker.style.left = "50%";
        marker.style.top = "25%";
        return marker;
    }

    let submit_button = document.getElementById("submit-button");
    if (!submit_button) {
        console.error("no submit button");
    }

    function update_submit() {
        if (unfinished_colors == 0) {
            submit_button.hidden = false;
        } else {
            submit_button.hidden = true;
        }
    }

    function add_marker(cell: HTMLTableCellElement, row_number: number, col_number: number, color: string) {
        if (color == null) {
            console.log("select a color before adding a marker");
            return;
        }

        if (cell.children.length != 0) {
            console.log("can't choose a tile twice");
            return;
        }

        if (color_usage.get(color) >= 2) {
            console.log("cannot select more then two places");
            return;
        } else if (color_usage.get(color) == 0) {
            unfinished_colors++;
        } else {
            unfinished_colors--;
        }

        cell.appendChild(getMarker(color));

        color_usage.set(color, color_usage.get(color) + 1);
    }

    function remove_marker(cell: HTMLTableCellElement, row_number: number, col_number: number) {
        if (cell.children.length == 0) {
            console.log("nothing to remove");
            return;
        }

        let marker = cell.children[0];
        const cell_color = window.getComputedStyle(marker).backgroundColor;
        console.log("removing color: " + cell_color);
        console.log("removing " + [row_number, col_number])
        if (color_usage.get(cell_color) == 0) {
            console.log("color non existent");
            return;
        } else if (color_usage.get(cell_color) == 1) {
            unfinished_colors--;
        } else {
            unfinished_colors++;
        }

        color_usage.set(cell_color, color_usage.get(cell_color) - 1);
        cell.removeChild(marker)
    }

    function select_element(cell: HTMLTableCellElement, row_number: number, col_number: number) {
        if (current_color == null) {
            remove_marker(cell, row_number, col_number);
        } else {
            add_marker(cell, row_number, col_number, current_color);
        }
        update_submit();
    }

    function build_element(row_number: number, col_number: number) {
        let element: HTMLTableCellElement = document.createElement("td");
        element.id = "coord: " + row_number.toString() + ", "
            + col_number.toString();
        element.className = "board-element";

        element.addEventListener("click", () => select_element(element, row_number, col_number));
        return element;
    }

    function build_row(row_number: number) {
        let row = document.createElement("tr");
        row.id = "row: " + row_number.toString();
        for (let column_number = 0; column_number < col_count; ++column_number) {
            row.appendChild(build_element(row_number, column_number));
        }
        return row;
    }

    function build_table() {
        for (let row_number = 0; row_number < row_count; row_number++) {
            table.appendChild(build_row(row_number));
        }

    }

    build_table();

    function add_previous_points() {
        const list = document.getElementById("original-dots");
        for (let i = 0; i < list.children.length; ++i) {
            const element = list.children[i];
            let row = parseInt(element.children[0].textContent);
            let col = parseInt(element.children[1].textContent);
            console.log(row + ", " + col);
            let color = element.children[2].textContent;
            let cell = table.children[row].children[col] as HTMLTableCellElement;
            add_marker(cell, row, col, color);
        }
    }

    add_previous_points();  
})


function serialize_points() {
    const points = [];
    for (let row_number = 0; row_number < row_count; row_number++) {
        const row = table.children[row_number] as HTMLTableRowElement;
        for (let col_number = 0; col_number < col_count; col_number++) {
            const cell = row.children[col_number] as HTMLTableCellElement;
            if (cell.children.length > 0) {
                const marker = cell.children[0] as HTMLElement;
                points.push({
                    row: row_number,
                    col: col_number,
                    color: marker.style.backgroundColor
                });
            }
        }
    }

    let input = document.getElementById("id_points") as HTMLTextAreaElement;
    if (!input) {
        console.error("input not found");
        return;
    }
    input.value = JSON.stringify(points);
}