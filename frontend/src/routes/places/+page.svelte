<script>
    import PlaceCard from '#lib/PlaceCard.svelte';
    
    let { data = {} } = $props();
    
    let areaNames = $derived(data?.areas ? Object.fromEntries(data.areas.map((a) => [a.area_id, a.area_name])) : {});
    let availablePrices = $derived([...new Set((data?.places || []).map(p => p.price_level).filter(Boolean))]);
    
    let selectedArea = $state('');
    let selectedPrice = $state('');
    
    let filteredPlaces = $derived.by(() => {
        let places = data?.places || [];
        if (selectedArea !== '') places = places.filter(p => p.area_id === Number(selectedArea));
        if (selectedPrice !== '') places = places.filter(p => p.price_level === selectedPrice);
        return places;
    });
</script>

<div class="mt-5">
    <p class="is-size-7 has-text-weight-bold mb-1" style="color: #ccff00;">FEATURED</p>
    <h1 class="title is-2 has-text-white mb-5">Explore Places</h1>
</div>

<!-- กล่องตัวกรอง (Filter) เหลือแค่ Area กับ Price -->
<div class="box mb-6" style="background-color: #1a1a1a;">
    <div class="columns is-mobile is-multiline">
        
        <!-- Select Area -->
        <div class="column is-12-mobile is-6-tablet">
            <div class="field">
                <div class="control">
                    <div class="select is-small is-fullwidth">
                        <select bind:value={selectedArea} style="background-color: #222; color: white; border: 1px solid #333;">
                            <option value="">Select area (all areas)</option>
                            {#each data?.areas || [] as area (area.area_id)}
                                <option value={area.area_id}>{area.area_name}</option>
                            {/each}
                        </select>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Select Price Range -->
        <div class="column is-12-mobile is-6-tablet">
            <div class="field">
                <div class="control">
                    <div class="select is-small is-fullwidth">
                        <select bind:value={selectedPrice} style="background-color: #222; color: white; border: 1px solid #333;">
                            <option value="">Price range (all ranges)</option>
                            {#each availablePrices as price}
                                <option value={price}>{price}</option>
                            {/each}
                        </select>
                    </div>
                </div>
            </div>
        </div>
        
    </div>
</div>

<div class="columns is-multiline">
    {#each filteredPlaces as item (item.place_id)}
        <div class="column is-4">
            <PlaceCard place={item} areaName={areaNames[item.area_id]} />
        </div>
    {:else}
        <p class="column has-text-grey">No places found matching your criteria.</p>
    {/each}
</div>