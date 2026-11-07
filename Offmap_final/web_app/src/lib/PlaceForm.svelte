<script>
    import { enhance } from '$app/forms';
    let { action, areas, submitLabel = 'Save' } = $props();
</script>

<form method="POST" {action} use:enhance={({ formElement }) => async ({ result, update }) => {
    await update();
    if (result.type === 'success') {
        formElement.reset();
    }
}}> 
    <input class="input is-small mb-2" name="place_name" placeholder="Place name" required />
    <div class="select is-small is-fullwidth mb-2">
        <select name="area_id" required>
            <option value="" disabled selected>Select area</option>
            {#each areas as area (area.area_id)}
                <option value={area.area_id}>{area.area_name}</option>
            {/each}
        </select>
    </div>
    <input class="input is-small mb-2" name="description" placeholder="Description" required />
    <input class="input is-small mb-2" name="address" placeholder="Address" required />
    <input class="input is-small mb-2" type="number" step="any" name="latitude" placeholder="Latitude" required />
    <input class="input is-small mb-2" type="number" step="any" name="longitude" placeholder="Longitude" required />
    <input class="input is-small mb-2" name="price_level" placeholder="200-1000 THB" required />
    <input class="input is-small mb-2" type="time" name="opening_time" required />
    <input class="input is-small mb-3" type="time" name="closing_time" required />
    <div class="buttons">
        <button class="button is-small has-text-weight-bold" style="background-color: #ccff00; color: black;">{submitLabel}</button>
    </div>
</form>