<script>
    import YourComponent from '#lib/YourComponent.svelte'

    const qa = {
        question: 'What is the capital of France?',
        answer: 'Paris'
    }

</script>
 
<h1>Props Example</h1>
 
<YourComponent question="1+1" answer="2" />
<YourComponent question="2+2" answer="4" />
<YourComponent question="3+3" answer="6" />
<YourComponent {...qa} />