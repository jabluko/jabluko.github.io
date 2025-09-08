"use strict";
document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("background-img-container");
    const image = document.getElementById("background-img");
    if (!image) {
        console.error("Image not found");
    }
    const formX = document.querySelector('input[name="x"]');
    if (!formX) {
        console.error("formX not found");
    }
    const formY = document.querySelector('input[name="y"]');
    if (!formY) {
        console.error("formY not found");
    }
    const form = (formX === null || formX === void 0 ? void 0 : formX.form) || (formY === null || formY === void 0 ? void 0 : formY.form);
    if (!form) {
        console.error("Form not found");
    }
    const pointRows = document.querySelectorAll("#point_table tbody tr");
    if (!pointRows) {
        console.error("Point rows not found");
    }
    image.addEventListener("click", function (event) {
        let x, y;
        if (typeof event.offsetX === "number" && typeof event.offsetY === "number") {
            x = event.offsetX;
            y = event.offsetY;
        }
        else {
            const rect = event.target.getBoundingClientRect();
            x = event.clientX - rect.left;
            y = event.clientY - rect.top;
        }
        if (formX)
            formX.value = x.toString();
        if (formY)
            formY.value = y.toString();
        console.log(`Clicked: X=${x}, Y=${y}`);
        if (form)
            form.submit();
    });
    let indicator = null;
    function showIndicator(x, y) {
        console.log(`Showing indicator at: X=${x}, Y=${y}`);
        if (indicator) {
            indicator.remove();
        }
        const rect = image.getBoundingClientRect();
        const containerRect = container.getBoundingClientRect();
        indicator = document.createElement("div");
        indicator.className = "point-indicator";
        indicator.style.left = `${x}px`;
        indicator.style.top = `${y}px`;
        container.appendChild(indicator);
    }
    function hideIndicator() {
        if (indicator) {
            indicator.remove();
            indicator = null;
        }
    }
    pointRows.forEach(row => {
        const xCell = row.querySelector("td:nth-child(1)");
        if (!xCell) {
            console.error("X cell not found in row", row);
            return;
        }
        const yCell = row.querySelector("td:nth-child(2)");
        if (!yCell) {
            console.error("Y cell not found in row", row);
            return;
        }
        const x = parseFloat(xCell.textContent || "0");
        const y = parseFloat(yCell.textContent || "0");
        row.addEventListener("mouseover", () => showIndicator(x, y));
        row.addEventListener("mouseout", hideIndicator);
        row.addEventListener("click", () => showIndicator(x, y));
    });
});
//# sourceMappingURL=pointOnBackground.js.map