<script>
    let { place, areaName } = $props();
</script>

<div class="card" style="background-color: #1a1a1a; border-radius: 12px; height: 100%;">
    <div class="card-content">
        <p class="is-size-7 has-text-weight-bold mb-1" style="color: #ccff00;">{areaName ?? 'Unknown area'}</p>
        <p class="title is-5 has-text-white mb-2">{place.place_name}</p>
        <p class="subtitle is-7 has-text-grey mb-4">{place.address}</p>
        
        <div class="content has-text-grey-light is-size-7">
            <p>{place.description}</p>
            <p class="mb-2">🕒 {place.opening_time} – {place.closing_time}</p>
            
            {#if place.price_level}
                <span class="tag has-text-weight-bold mt-2" style="background-color: #ccff00; color: black;">
                    {place.price_level}
                </span>
            {:else}
                <span class="tag is-dark has-text-grey mt-2">No price data</span>
            {/if}
        </div>
    </div>
</div>