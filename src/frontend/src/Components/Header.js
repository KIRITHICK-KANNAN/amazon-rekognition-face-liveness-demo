import React from "react";

function Header() {
  return (
    <>
      <nav
        class="navbar navbar-expand-sm navbar-dark border-bottom bg-header fixed-top"
        style="background: #f8f9fa; box-shadow: 0 0 1rem rgba(0, 0, 0, 0.2); padding: 0.8rem 0.8rem; margin-bottom: 1.5rem;"
      >
        <div class="container">
          <a class="navbar-brand" href="index.html">
            <img
              src="https://vfseu.mioot.com/forms/DEV/ITSLT/Design/Dha_Appointment/img/vfs_logo3.png"
              alt="logo"
              class="site_logo img-fluid"
              style="max-width: 100%; height: auto; width: 10%;"
            />
          </a>
        </div>
      </nav>
    </>
  );
}

export default Header;
