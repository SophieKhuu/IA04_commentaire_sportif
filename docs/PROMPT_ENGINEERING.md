# Prompt Engineering Guide

## System Prompt

The system prompt is crucial for accurate volleyball analysis. Located in `src/config.py`:

```python
SYSTEM_PROMPT_VOLLEYBALL = """Tu es un expert en analyse de volleyball..."""
```

## Current Prompt (v1.0)

```
Tu es un expert en analyse de volleyball avec 20+ ans d'expérience.
Tu dois analyser des commentaires sportifs de volleyball et extraire 
les informations suivantes en JSON valide:

1. Résumé (1-2 phrases): les faits clés du commentaire
2. Joueurs identifiés: liste des noms/numéros
3. Pour chaque joueur:
   - Technique (0-100)
   - Défense (0-100)
   - Attitude (0-100)
   - Physique (0-100)
   - Décision_tactique (0-100)
   - Autre (0-100)
   - Résumé: observation narrative

Réponds UNIQUEMENT en JSON valide sans commentaires additionnels.
```

## Optimization Tips

### 1. Be More Specific About Scoring

**Current:**
```
Technique (0-100): maîtrise technique
```

**Better:**
```
Technique (0-100): Évaluer la précision des passes, la qualité des frappes, 
la maîtrise du placement. 0=inexperienced, 50=average, 100=elite professional
```

### 2. Add Examples (Few-shot Learning)

```
Exemple:
Entrée: "Dupont a fait un excellent match avec des passes précises"
Sortie: {
  "players": [{"name": "Dupont", "technique": 85, "defense": 78, ...}]
}
```

### 3. Clarify Ambiguities

```
Pour "attitude", incluez:
- Leadership et communication
- Respect des règles
- Réaction face à l'adversité
- Soutien aux coéquipiers
```

### 4. Handle Edge Cases

```
Si le commentaire ne mentionne pas un joueur pour un critère:
- Ne pas inventer de score
- Utiliser 50 (neutre) ou expliquer l'absence
```

## Testing Different Prompts

### Version Comparison Template

```
SYSTEM_PROMPT_V1 = "..."
SYSTEM_PROMPT_V2 = "..."

# Test on sample_commentaries.json
for commentary in samples:
    result_v1 = llm_client.analyze_commentary(commentary, prompt=V1)
    result_v2 = llm_client.analyze_commentary(commentary, prompt=V2)
    compare(result_v1, result_v2)
```

## Common Issues & Solutions

### Issue: LLM Generates Non-JSON Response

**Solution**: Add to prompt:
```
IMPORTANT: Répondez UNIQUEMENT avec du JSON valide.
N'ajoutez PAS d'explications texte avant ou après le JSON.
```

### Issue: Scores Not 0-100 Range

**Solution**: 
```
Chaque score DOIT être un entier entre 0 et 100.
0 = très faible, 50 = moyen, 100 = exceptionnel.
```

### Issue: Players Not Identified

**Solution**: 
```
Identifiez TOUS les joueurs mentionnés par:
- Nom complet ou partiel
- Numéro de maillot
- Surnom ou position
```

### Issue: Hallucinated Players/Facts

**Solution**:
```
Ne créez PAS de joueurs ou d'actions non mentionnés dans le commentaire.
Extrayez UNIQUEMENT ce qui est explicitement écrit.
```

## Language Support

### French (Current)
```
SYSTEM_PROMPT_VOLLEYBALL (French version)
```

### English Version

```python
SYSTEM_PROMPT_VOLLEYBALL_EN = """You are an expert volleyball analyst with 20+ years experience.
Analyze volleyball sports commentary and extract information in valid JSON:

1. Summary (1-2 sentences): key facts
2. Identified players: list of names/numbers
3. For each player:
   - Technique (0-100): passing, spiking accuracy
   - Defense (0-100): blocking, recovery efficiency
   - Attitude (0-100): mental engagement, behavior
   - Physique (0-100): physical performance, explosivity
   - Decision_tactique (0-100): tactical decision-making, game reading
   - Autre (0-100): other observations
   - Notes: narrative summary

Respond ONLY with valid JSON, no additional text.
"""
```

## Customization by Sport Level

### Amateur/Recreational Level

Add to prompt:
```
Ce commentaire analyse un match amateur.
Considérez les erreurs techniques comme normales.
Évaluez la progression plutôt que la perfection.
```

### Professional Level

Add to prompt:
```
Ce commentaire analyse un match de niveau professionnel.
Appliquez des critères de haute performance.
Identifiez les erreurs stratégiques.
```

## Fine-Tuning Strategy

### Step 1: Baseline
- Use current prompt
- Test on 5-10 commentaries
- Record average score & variance

### Step 2: Identify Issues
- Which scores are consistently wrong?
- Which players are missed?
- Is JSON always valid?

### Step 3: Modify & Test
- Change one prompt aspect
- Test on same 5-10 samples
- Compare metrics

### Step 4: Validate
- Test on NEW commentaries
- Check consistency
- Measure improvement

### Step 5: Deploy
- Update `src/config.py`
- Document changes
- Archive old version

## Prompt Versioning

```python
# In config.py
SYSTEM_PROMPT_VERSIONS = {
    "v1.0": "...",  # Original
    "v1.1": "...",  # Added examples
    "v1.2": "...",  # Better criteria definitions
    "v2.0": "...",  # Major revision
}

SYSTEM_PROMPT_VOLLEYBALL = SYSTEM_PROMPT_VERSIONS["v2.0"]
```

## Evaluation Metrics

### Accuracy
- Do extracted player names match commentary?
- Are scores within expected range (0-100)?

### Fidelity
- Does analysis match human interpretation?
- Are key facts preserved?

### Consistency
- Same commentary → same result (if same LLM)?
- Different commentaries → different scores?

### JSON Quality
- Valid JSON 100% of the time?
- Required fields always present?

## Resources

- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Few-shot Learning](https://openai.com/research/gpt-3)
- [Prompt Injection Prevention](https://owasp.org/www-community/attacks/Prompt_Injection)

## Contribution

To improve prompts:
1. Create new version in `config.py`
2. Test with `tests/test_prompt_*.py`
3. Document changes here
4. Submit PR

---

**Last Updated**: April 2024
**Current Version**: v1.0
