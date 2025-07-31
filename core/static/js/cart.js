// static/js/cart-utils.js
export async function fetchCartItems() {
  const token = localStorage.getItem("access_token");

  if (!token) {
    console.error("No access token found, user might not be logged in");
    return [];
  }
  try {
    const response = await fetch("/api/customer-cart-items/", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch cart");
    }

    const data = await response.json();
    console.log("Cart data:", data);

    if (data.length === 0) {
      console.log("No carts found for user");
      return [];
    }

    return data;
  } catch (error) {
    console.error("Error fetching cart:", error);
    return [];
  }
}
