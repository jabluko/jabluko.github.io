var Sidebar = /** @class */ (function () {
    function Sidebar() {
    }
    Sidebar.init = function (barId, mainId) {
        var gotSide = document.getElementById(barId);
        if (!gotSide) {
            console.error("Sidebar element not found");
            return;
        }
        this.sidebar = gotSide;
        this.sidebarWidth = parseInt(getComputedStyle(this.sidebar).width, 10);
        var gotMain = document.getElementById(mainId);
        if (!gotMain) {
            console.error("Sidebar element not found");
            return;
        }
        this.main = gotMain;
        this.mainWidth = parseInt(getComputedStyle(this.main).width, 10);
    };
    Sidebar.display = function () {
        this.sidebar.style.width = new String(this.sidebarWidth) + "px";
        this.main.style.width = new String(this.mainWidth - this.sidebarWidth) + "px";
    };
    Sidebar.hide = function () {
        this.sidebar.style.width = "0px";
        this.main.style.width = new String(this.mainWidth) + "px";
    };
    Sidebar.toggle = function () {
        if (!this.sidebar || !this.main) {
            console.error("Sidebar not initialized properly");
            return;
        }
        var curWidth = parseInt(getComputedStyle(this.sidebar).width, 10);
        if (curWidth === this.sidebarWidth) {
            this.hide();
        }
        else {
            this.display();
        }
    };
    Sidebar.sidebarWidth = 0;
    Sidebar.mainWidth = 0;
    return Sidebar;
}());
function setUpSidebar() {
    Sidebar.init("sidebar", "right-to-sidebar");
    Sidebar.display();
    console.log("Setup complete");
}
