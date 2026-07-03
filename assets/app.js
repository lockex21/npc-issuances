const searchInput = document.querySelector("#search-input")
const kindFilter = document.querySelector("#kind-filter")
const yearFilter = document.querySelector("#year-filter")
const cards = Array.from(document.querySelectorAll(".issuance-card"))

function applyFilters() {
  const search = (searchInput?.value || "").trim().toLowerCase()
  const kind = kindFilter?.value || ""
  const year = yearFilter?.value || ""

  cards.forEach((card) => {
    const text = card.textContent.toLowerCase()
    const kindMatch = !kind || card.dataset.kind === kind
    const yearMatch = !year || card.dataset.year === year
    const searchMatch = !search || text.includes(search)
    card.classList.toggle("is-hidden", !(kindMatch && yearMatch && searchMatch))
  })
}

searchInput?.addEventListener("input", applyFilters)
kindFilter?.addEventListener("change", applyFilters)
yearFilter?.addEventListener("change", applyFilters)
