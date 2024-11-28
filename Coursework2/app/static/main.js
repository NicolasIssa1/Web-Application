document.addEventListener("DOMContentLoaded", () => {
    console.log("JavaScript Loaded!");

    // Home Page Hover Animation
    const homepageText = document.querySelector(".homepage-text");
    if (homepageText) {
        console.log("Homepage text element found.");
        homepageText.style.transition = "all 0.3s ease-in-out";
        homepageText.addEventListener("mouseover", () => {
            homepageText.style.color = "#0073b1"; // LinkedIn blue
            homepageText.style.transform = "scale(1.05)";
        });
        homepageText.addEventListener("mouseout", () => {
            homepageText.style.color = "black";
            homepageText.style.transform = "scale(1)";
        });
    } else {
        console.log("Homepage text element not found. Skipping hover animation.");
    }

    // Smooth Dropdown Animation for User Menu
    const dropdownToggle = document.querySelector(".dropdown-toggle");
    if (dropdownToggle) {
        console.log("Dropdown toggle found.");
        dropdownToggle.addEventListener("click", () => {
            const dropdownMenu = dropdownToggle.nextElementSibling;
            if (dropdownMenu.style.display === "block") {
                dropdownMenu.style.opacity = "0";
                setTimeout(() => {
                    dropdownMenu.style.display = "none";
                }, 300); // Smooth fade-out duration
            } else {
                dropdownMenu.style.display = "block";
                dropdownMenu.style.opacity = "0";
                dropdownMenu.style.animation = "fadeIn 0.3s ease-in-out";
                setTimeout(() => {
                    dropdownMenu.style.opacity = "1";
                }, 10);
            }
        });
    } else {
        console.log("Dropdown toggle not found.");
    }

    // Modal for Viewing Profile Picture
    const viewProfilePictureBtn = document.getElementById("view-profile-picture-btn");
    const profilePictureModalElement = document.getElementById("profile-picture-modal");

    if (viewProfilePictureBtn && profilePictureModalElement) {
        console.log("View Profile Picture button and modal found.");
        const profilePictureModal = new bootstrap.Modal(profilePictureModalElement);

        viewProfilePictureBtn.addEventListener("click", () => {
            profilePictureModal.show();
        });
    } else {
        console.log("View Profile Picture button or modal not found.");
    }

    // Live Character Counter for Profile Fields
    const textareas = document.querySelectorAll("textarea");
    if (textareas.length > 0) {
        console.log(`${textareas.length} textarea(s) found.`);
        textareas.forEach((textarea) => {
            const counter = document.createElement("small");
            counter.className = "char-counter";
            counter.style.display = "block";
            counter.style.marginTop = "5px";
            counter.style.fontSize = "12px";
            textarea.parentElement.appendChild(counter);
            textarea.addEventListener("input", () => {
                const maxLength = textarea.getAttribute("maxlength") || 500;
                counter.textContent = `${textarea.value.length}/${maxLength} characters`;
                counter.style.color = textarea.value.length > maxLength ? "red" : "gray";
            });
        });
    } else {
        console.log("No textareas found.");
    }

    // Enable or Disable the Update Profile Button
    const profileForm = document.querySelector("#profile_form");
    if (profileForm) {
        console.log("Profile form found.");
        const updateButton = profileForm.querySelector("button[type='submit']");
        profileForm.addEventListener("input", () => {
            let isValid = true;
            const formTextareas = profileForm.querySelectorAll("textarea");
            formTextareas.forEach((textarea) => {
                if (textarea.value.trim() === "") {
                    isValid = false;
                }
            });
            updateButton.disabled = !isValid;
        });
    } else {
        console.log("Profile form not found.");
    }

    // Dynamic Skill Adding and Removing Feature
    const skillContainer = document.querySelector("#skills_container");
    const skillInput = document.querySelector("#skills_input");
    const addSkillButton = document.querySelector("#add_skill_button");
    const skillsHiddenInput = document.querySelector("#skills_hidden_input");

    if (skillContainer && skillInput && addSkillButton && skillsHiddenInput) {
        console.log("Dynamic skill adding feature elements found.");

        // Function to update the hidden input value
        const updateSkillsInput = () => {
            const skillBadges = skillContainer.querySelectorAll(".skill-badge");
            const skills = Array.from(skillBadges).map((badge) => badge.textContent.trim());
            skillsHiddenInput.value = skills.join(",");
        };

        addSkillButton.addEventListener("click", (e) => {
            e.preventDefault();
            const skill = skillInput.value.trim();
            if (skill) {
                const skillTag = document.createElement("span");
                skillTag.className = "badge bg-primary mx-1 skill-badge";
                skillTag.textContent = skill;

                // Add remove button to each skill tag
                const removeButton = document.createElement("button");
                removeButton.type = "button";
                removeButton.className = "btn-close ms-2 remove-skill-btn";
                removeButton.style.fontSize = "0.8rem";
                removeButton.addEventListener("click", () => {
                    skillTag.remove();
                    updateSkillsInput(); // Update the hidden input when a skill is removed
                });

                skillTag.appendChild(removeButton);
                skillContainer.appendChild(skillTag);

                // Clear input and update hidden input
                skillInput.value = "";
                updateSkillsInput();
            }
        });

        // Allow removing skills dynamically
        skillContainer.addEventListener("click", (e) => {
            if (e.target.classList.contains("remove-skill-btn")) {
                const skillTag = e.target.closest(".skill-badge");
                if (skillTag) {
                    skillTag.remove();
                    updateSkillsInput();
                }
            }
        });

        // Initialize hidden input value on page load
        updateSkillsInput();
    } else {
        console.log("Dynamic skill adding feature elements not found.");
    }

    // Profile Completion Progress Bar
    const progressBar = document.querySelector("#profile-completion-bar");
    if (progressBar) {
        const updateProgressBar = () => {
            let completedFields = 0;
            const totalFields = 5; // Adjust based on total required fields
            const fieldsToCheck = [
                "name",
                "bio",
                "education",
                "skills_hidden_input",
                "work_experience",
            ];

            fieldsToCheck.forEach((fieldId) => {
                const field = document.getElementById(fieldId);
                if (field && field.value.trim()) {
                    completedFields++;
                }
            });

            const completionPercentage = Math.round((completedFields / totalFields) * 100);
            progressBar.style.width = `${completionPercentage}%`;
            progressBar.setAttribute("aria-valuenow", completionPercentage);
            progressBar.textContent = `${completionPercentage}%`;
        };

        // Update progress bar on form input
        profileForm.addEventListener("input", updateProgressBar);

        // Initialize progress bar on page load
        updateProgressBar();
    } else {
        console.log("Progress bar not found.");
    }
});
