document.addEventListener("DOMContentLoaded", () => {
  // Dark mode toggle
  const darkModeToggle = document.getElementById("darkModeToggle")
  const body = document.body

  // Check for saved dark mode preference
  if (localStorage.getItem("darkMode") === "enabled") {
    body.classList.add("dark-mode")
    updateDarkModeIcon(true)
  }

  if (darkModeToggle) {
    darkModeToggle.addEventListener("click", () => {
      body.classList.toggle("dark-mode")
      const isDarkMode = body.classList.contains("dark-mode")

      if (isDarkMode) {
        localStorage.setItem("darkMode", "enabled")
      } else {
        localStorage.setItem("darkMode", "disabled")
      }

      updateDarkModeIcon(isDarkMode)
    })
  }

  function updateDarkModeIcon(isDarkMode) {
    const icon = darkModeToggle.querySelector("i")
    if (isDarkMode) {
      icon.className = "fas fa-sun"
    } else {
      icon.className = "fas fa-moon"
    }
  }

  // Habit toggle functionality
  const habitToggles = document.querySelectorAll(".habit-toggle")
  habitToggles.forEach((toggle) => {
    toggle.addEventListener("change", function () {
      const habitId = this.dataset.habitId
      const isCompleted = this.checked

      // Add loading state
      this.disabled = true
      const card = this.closest(".habit-card")
      card.classList.add("loading")

      fetch(`/toggle/${habitId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          completed: isCompleted,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            // Update streak counter
            const streakBadge = card.querySelector(".badge.bg-primary")
            if (streakBadge) {
              streakBadge.innerHTML = `<i class="fas fa-fire me-1"></i>${data.streak} day streak`
            }

            // Update progress bar
            const progressBar = card.querySelector(".progress-bar")
            if (progressBar) {
              progressBar.style.width = `${data.progress}%`
            }

            const progressText = card.querySelector(".progress").parentElement.querySelector("small:last-child")
            if (progressText) {
              progressText.textContent = `${Math.round(data.progress)}%`
            }

            // Add success animation
            card.classList.add("success-animation")
            setTimeout(() => {
              card.classList.remove("success-animation")
            }, 300)

            // Show success message
            showToast(isCompleted ? "Habit completed! 🎉" : "Habit unchecked", "success")
          } else {
            // Revert checkbox state
            this.checked = !isCompleted
            showToast("Error updating habit", "error")
          }
        })
        .catch((error) => {
          console.error("Error:", error)
          this.checked = !isCompleted
          showToast("Error updating habit", "error")
        })
        .finally(() => {
          this.disabled = false
          card.classList.remove("loading")
        })
    })
  })

  // Habit notes functionality
  const habitNotes = document.querySelectorAll(".habit-notes")
  habitNotes.forEach((textarea) => {
    let timeout

    textarea.addEventListener("input", function () {
      clearTimeout(timeout)
      const habitId = this.dataset.habitId
      const notes = this.value

      // Debounce the API call
      timeout = setTimeout(() => {
        fetch(`/notes/${habitId}/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: `notes=${encodeURIComponent(notes)}`,
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              // Visual feedback for successful save
              this.style.borderColor = "#28a745"
              setTimeout(() => {
                this.style.borderColor = ""
              }, 1000)
            }
          })
          .catch((error) => {
            console.error("Error saving notes:", error)
          })
      }, 1000) // Wait 1 second after user stops typing
    })
  })

  // Auto-resize textareas
  habitNotes.forEach((textarea) => {
    textarea.addEventListener("input", function () {
      this.style.height = "auto"
      this.style.height = this.scrollHeight + "px"
    })

    // Initial resize
    textarea.style.height = "auto"
    textarea.style.height = textarea.scrollHeight + "px"
  })

  // Toast notification system
  function showToast(message, type = "info") {
    const toastContainer = getOrCreateToastContainer()

    const toast = document.createElement("div")
    toast.className = `toast align-items-center text-white bg-${type === "error" ? "danger" : "success"} border-0`
    toast.setAttribute("role", "alert")
    toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `

    toastContainer.appendChild(toast)

    const bsToast = window.bootstrap.Toast // Declare bootstrap variable
    new bsToast(toast).show()

    // Remove toast element after it's hidden
    toast.addEventListener("hidden.bs.toast", () => {
      toast.remove()
    })
  }

  function getOrCreateToastContainer() {
    let container = document.getElementById("toast-container")
    if (!container) {
      container = document.createElement("div")
      container.id = "toast-container"
      container.className = "toast-container position-fixed bottom-0 end-0 p-3"
      container.style.zIndex = "1055"
      document.body.appendChild(container)
    }
    return container
  }

  // CSRF token helper
  function getCookie(name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";")
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim()
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
          break
        }
      }
    }
    return cookieValue
  }

  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault()
      const target = document.querySelector(this.getAttribute("href"))
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        })
      }
    })
  })

  // Auto-dismiss alerts after 5 seconds
  const alerts = document.querySelectorAll(".alert:not(.alert-permanent)")
  alerts.forEach((alert) => {
    setTimeout(() => {
      const bsAlert = window.bootstrap.Alert // Declare bootstrap variable
      new bsAlert(alert).close()
    }, 5000)
  })

  // Initialize tooltips
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  tooltipTriggerList.map((tooltipTriggerEl) => {
    return new window.bootstrap.Tooltip(tooltipTriggerEl) // Declare bootstrap variable
  })

  // Initialize popovers
  const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
  popoverTriggerList.map((popoverTriggerEl) => {
    return new window.bootstrap.Popover(popoverTriggerEl) // Declare bootstrap variable
  })
})

// Utility function to format dates
function formatDate(date) {
  return new Intl.DateTimeFormat("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  }).format(date)
}

// Utility function to calculate days between dates
function daysBetween(date1, date2) {
  const oneDay = 24 * 60 * 60 * 1000
  return Math.round(Math.abs((date1 - date2) / oneDay))
}

// Service Worker registration for offline functionality (optional)
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .register("/sw.js")
      .then((registration) => {
        console.log("ServiceWorker registration successful")
      })
      .catch((error) => {
        console.log("ServiceWorker registration failed")
      })
  })
}
