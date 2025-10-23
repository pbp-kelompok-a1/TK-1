$(document).ready(function () {
    loadFollowedSports();

    // Load current following list
    function loadFollowedSports() {
        $.ajax({
            url: "/api/following/",
            method: "GET",
            success: function (response) {
                $("#following-list").empty();
                response.forEach(function (sport) {
                    $("#following-list").append(`
                        <div class="sport-tag" data-id="${sport.id}">
                            ${sport.name}
                            <button class="unfollow-btn">×</button>
                        </div>
                    `);
                });
            },
            error: function () {
                alert("Failed to load followed sports.");
            }
        });
    }

    // Unfollow sport
    $(document).on("click", ".unfollow-btn", function () {
        const sportId = $(this).parent().data("id");
        $.ajax({
            url: `/api/following/${sportId}/`,
            method: "DELETE",
            success: function () {
                loadFollowedSports();
            },
            error: function () {
                alert("Could not unfollow this sport.");
            }
        });
    });

    // Follow a new sport (mock prompt for simplicity)
    $("#follow-sport-btn").on("click", function () {
        const newSport = prompt("Enter sport name to follow:");
        if (!newSport) return;

        $.ajax({
            url: "/api/following/",
            method: "POST",
            data: JSON.stringify({ name: newSport }),
            contentType: "application/json",
            success: function () {
                loadFollowedSports();
            },
            error: function () {
                alert("Failed to follow this sport.");
            }
        });
    });

    // Save changes button (example placeholder)
    $("#save-btn").on("click", function () {
        alert("Changes saved successfully!");
    });
});
