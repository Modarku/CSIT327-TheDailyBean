function searchProducts() {
    const searchTerm = document.getElementById("searchInput").value.toLowerCase();
    const products = document.querySelectorAll(".product-card");

    products.forEach((product) => {
        const productName = product.getAttribute("data-name").toLowerCase();
        product.style.display = productName.includes(searchTerm) ? "block" : "none";
    });
}
