class Sidebar {
    static sidebar: HTMLElement;
    static main: HTMLElement;
    static sidebarWidth: number = 0;
    static mainWidth: number = 0;

    static init(barId: string, mainId: string) {
        let gotSide = document.getElementById(barId);
        if (!gotSide) {
            console.error("Sidebar element not found");
            return;
        }
        this.sidebar = gotSide;
        this.sidebarWidth = parseInt(getComputedStyle(this.sidebar).width, 10);

        let gotMain = document.getElementById(mainId);

        if (!gotMain) {
            console.error("Sidebar element not found");
            return;
        }
        this.main = gotMain; 
        this.mainWidth = parseInt(getComputedStyle(this.main).width, 10);
    }

    static display(): void {
        this.sidebar.style.width = new String(this.sidebarWidth) + "px";
        this.main.style.width = new String(this.mainWidth - this.sidebarWidth) + "px";
    }

    static hide(): void {
        this.sidebar.style.width = "0px";
        this.main.style.width = new String(this.mainWidth) + "px";
    }

    static toggle(): void {
        if (!this.sidebar || !this.main) {
            console.error("Sidebar not initialized properly");
            return;
        }

        let curWidth = parseInt(getComputedStyle(this.sidebar).width, 10);

        if (curWidth === this.sidebarWidth) {
            this.hide()
        } else {
            this.display();
        }
    }
}

function setUpSidebar(): void {
    Sidebar.init("sidebar", "right-to-sidebar");
    Sidebar.display();
    console.log("Setup complete");
}