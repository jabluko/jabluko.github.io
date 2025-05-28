
let table: HTMLTableElement | null = null;
let row_count: number = 0;
let col_count: number = 0;
let color_usage = new Map<String, number>;
let current_color: string | null = null

let unfinished_colors = 0;


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

function update_submit() {
    let submit_button = document.getElementById("submit-button");
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
        unfinished_colors++; build_table
    }

    color_usage.set(cell_color, color_usage.get(cell_color) - 1);
    cell.removeChild(marker)
}

function build_element(row_number: number, col_number: number) {
    let element: HTMLTableCellElement = document.createElement("td");
    element.id = "coord: " + row_number.toString() + ", "
        + col_number.toString();
    element.className = "board-element";
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
    table = document.getElementById("board-table") as HTMLTableElement;
    row_count = parseInt(document.getElementById("rows").textContent)
    col_count = parseInt(document.getElementById("cols").textContent)

    if (!table) {
        console.error("table not found");
    }
    for (let row_number = 0; row_number < row_count; row_number++) {
        table.appendChild(build_row(row_number));
    }

}

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