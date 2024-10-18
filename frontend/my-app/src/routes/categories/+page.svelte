<script>
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { checkToken, checkRole } from "$lib/utils/auth.js";
  import { showNotification } from "$lib/stores/popupStore.js";
  import CategoryCard from "$lib/components/cards/CategoryCard.svelte";
  import CategoryFilterPanel from "$lib/components/FilterPanels/CategoryFilterPanel.svelte";
  import AddWindowPopup from "$lib/components/Popups/WindowPopups/Category/AddWindowPopup.svelte";
  import EditWindowPopup from "$lib/components/Popups/WindowPopups/Category/EditWindowPopup.svelte";
  import { ListFilter, Trash, X, Plus } from "lucide-svelte";
  import GeneralDeleteWidnowPopup from "../../lib/components/Popups/WindowPopups/GeneralDeleteWidnowPopup.svelte";

  //Data displayed
  let categories = [];

  //User validation
  let isValid = false;
  let hasAccess = false;
  const expectedRoles = ["admin"];

  //Popup
  let errorMessage = "";

  //User interaction
  let showPopupWindow = false;
  let popupType = "";
  let selectedCategory = null;
  let isProccessing = true;
  let isDeletionMode = false;

  onMount(async () => {
    isProccessing = true;
    const { isValid: valid, error } = await checkToken();
    if (!valid) {
      errorMessage = error;
      if (error === "Your account is pending approval") {
        goto("/pending-approval");
      } else {
        goto("/login");
      }
    }

    if (valid) {
      hasAccess = await checkRole(expectedRoles);
    }
    if (!hasAccess) {
      errorMessage = "You do not have access to this page.";
      goto("/login");
    } else {
      isValid = true;
      await fetchCategories();
    }

    if (!isValid) {
      showNotification(errorMessage, "error");
    }
    isProccessing = false;
  });

  //API calls
  async function fetchCategories(filters = {}) {
    isProccessing = true;
    let queryParams = "";
    const params = new URLSearchParams();

    if (filters.name) params.append("name", filters.name);
    if (filters.ascending !== undefined)
      params.append("ascending", filters.ascending);

    queryParams = params.toString();
    try {
      const response = await fetch(
        `http://localhost:8000/api/admin/categories?${queryParams}`,
        {
          method: "GET",
          headers: {
            Accept: "application/json",
            Authorization: `Bearer ${localStorage.getItem("authToken")}`,
          },
        },
      );

      if (!response.ok) {
        const errorData = await response.json();
        if (response.status === 403) {
          showNotification(
            "You do not have permission to fetch categories",
            "error",
          );
          goto("/login");
        } else {
          errorMessage =
            errorData.detail || "An error occurred. Please try again.";
          showNotification(errorMessage, "error");
        }
      } else {
        categories = await response.json();
      }
    } catch (error) {
      console.error("Error occurred while fetching categories:", error);
      showNotification("An error occurred. Please try again.", "error");
    }
    isProccessing = false;
  }

  async function addCategory(categoryName) {
    isProccessing = true;
    if (categoryName.trim()) {
      try {
        const response = await fetch(`http://localhost:8000/api/categories`, {
          method: "POST",
          headers: {
            Accept: "application/json",
            Authorization: `Bearer ${localStorage.getItem("authToken")}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ category_name: categoryName }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          if (errorData.status === 403) {
            showNotification(
              "You do not have permission to add categories",
              "error",
            );
            goto("/login");
          } else if (errorData.status === 409) {
            showNotification("Category already exists", "error");
          } else {
            showNotification(
              errorData.detail || "Failed to add category",
              "error",
            );
          }
        } else {
          showNotification("Category added", "success");
          await fetchCategories();
        }
      } catch (error) {
        console.error("Error occurred while creating category:", error);
        showNotification("An error occurred. Please try again.", "error");
      }
    }
    isProccessing = false;
  }

  async function deleteCategory() {
    isProccessing = true;
    try {
      const response = await fetch(
        `http://localhost:8000/api/categories/${selectedCategory.id}`,
        {
          method: "DELETE",
          headers: {
            Accept: "application/json",
            Authorization: `Bearer ${localStorage.getItem("authToken")}`,
          },
        },
      );

      if (!response.ok) {
        const errorData = await response.json();

        if (errorData.status === 403) {
          showNotification(
            "You do not have permission to add categories",
            "error",
          );
          goto("/login");
        } else if (errorData.status === 404) {
          showNotification("Category not found", "error");
        } else {
          showNotification(errorData.detail || "Failed to add user", "error");
        }
      } else {
        showNotification("Category deleted successfully", "success");
        await fetchCategories();
      }
    } catch (error) {
      console.error("Error occurred while deleting category:", error);
      showNotification("An error occurred. Please try again.", "error");
    }
    isProccessing = false;
  }

  async function updateCategory(categoryName) {
    isProccessing = true;
    if (categoryName.trim()) {
      try {
        const response = await fetch(
          `http://localhost:8000/api/categories/${selectedCategory.id}`,
          {
            method: "PUT",
            headers: {
              Accept: "application/json",
              Authorization: `Bearer ${localStorage.getItem("authToken")}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              category_name: categoryName,
              category_id: selectedCategory.id,
            }),
          },
        );

        if (!response.ok) {
          const errorData = await response.json();

          if (errorData.status === 403) {
            showNotification(
              "You do not have permission to add categories",
              "error",
            );
            goto("/login");
          } else if (errorData.status === 404) {
            showNotification("Category not found", "error");
          } else {
            showNotification(
              errorData.detail || "Failed to updade category",
              "error",
            );
          }
        } else {
          showNotification("Category updated successfully", "success");
          await fetchCategories();
        }
      } catch (error) {
        console.error("Error occurred while updating category:", error);
        showNotification("An error occurred. Please try again.", "error");
      }
    } else {
      showNotification("Category name cannot be empty", "error");
    }
    isProccessing = false;
  }

  function toggleDeletionMode() {
    isDeletionMode = !isDeletionMode;
  }

  function toggleWindowPopup(category, popup) {
    selectedCategory = category;
    popupType = popup;
    if (popup) showPopupWindow = true;
    else showPopupWindow = false;
  }
</script>

<div class="action-button-container">
  <button
    class="action-button"
    on:click={() => toggleWindowPopup(null, "filter")}
  >
    <ListFilter />
  </button>
  <button
    class="action-button"
    on:click={() => toggleWindowPopup(null, "addCategory")}
  >
    <Plus />
  </button>
  <button class="action-button" on:click={toggleDeletionMode}>
    {#if isDeletionMode}
      <X />
    {:else}
      <Trash />
    {/if}
  </button>
</div>

{#if showPopupWindow}
  {#if popupType === "addCategory"}
    <AddWindowPopup
      onAdd={addCategory}
      onClose={() => toggleWindowPopup(null, "")}
    />
  {:else if popupType === "deleteCategory"}
    <GeneralDeleteWidnowPopup
      header="Delete category?"
      label="Category"
      data={selectedCategory.name}
      onDelete={deleteCategory}
      onClose={() => toggleWindowPopup(null, "")}
    />
  {:else if popupType === "editCategory"}
    <EditWindowPopup
      categoryName={selectedCategory.name}
      onEdit={updateCategory}
      onClose={() => toggleWindowPopup(null, "")}
    />
  {:else if popupType === "filter"}
    <CategoryFilterPanel
      toggleFilterMenu={() => toggleWindowPopup(null, "")}
      applyFilter={fetchCategories}
    />
  {/if}
{/if}

{#if isProccessing}
  <div class="loading-circle"></div>
{:else if categories.length === 0}
  <p>No categoreis found.</p>
{:else}
  <div class="center-container">
    <div class="card-container">
      {#each categories as category}
        <CategoryCard {category} {isDeletionMode} {toggleWindowPopup} />
      {/each}
    </div>
  </div>
{/if}
