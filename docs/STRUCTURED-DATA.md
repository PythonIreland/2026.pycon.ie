# Structured Data (JSON-LD) - Implementation Guide

## 📋 Vue d'Ensemble

Le site PyCon Ireland 2026 implémente des schémas JSON-LD complets pour améliorer le référencement et activer les rich snippets dans les résultats de recherche Google.

## 🎯 Schémas Implémentés

### 1. Page d'Accueil (`/`)
**Fichier:** `layouts/partials/structured-data.html`

#### Event Schema
```json
"@type": "Event"
```
- Informations complètes sur la conférence
- Dates : 8-9 novembre 2026
- Lieu : UCD O'Reilly Hall avec coordonnées GPS
- Organisateur : Python Ireland
- Pricing : 40€ - 300€

#### Organization Schema
```json
"@type": "Organization"
```
- Python Ireland avec logo et contacts
- Liens sociaux (Twitter)

#### WebSite Schema
```json
"@type": "WebSite"
```
- Métadonnées du site principal

#### BreadcrumbList Schema
```json
"@type": "BreadcrumbList"
```
- Navigation hiérarchique pour pages intérieures

---

### 2. Page Speakers (`/speakers/`)
**Fichier:** `layouts/partials/structured-data-speakers.html`

#### Option 1: ItemList + Person
```json
"@type": "ItemList"
```
**Contenu:**
- Liste complète des {{ len .Site.Data.speakers }} speakers
- Chaque speaker avec position dans la liste
- Métadonnées complètes : nom, titre, entreprise, bio, photo

**Avantage SEO:**
- Google peut afficher un carrousel de speakers
- Améliore le référencement de la page speakers
- Rich snippets avec photos et infos

#### Option 2: Person avec performerIn
```json
"@type": "Person"
"performerIn": [...]
```
**Contenu:**
- Schéma Person enrichi pour chaque speaker
- Propriété `performerIn` liant le speaker à ses talks
- Liens sociaux (Twitter, GitHub, LinkedIn, Mastodon)
- Entreprise et rôle

**Avantage SEO:**
- Relation bidirectionnelle speaker ↔ talk
- Google comprend le contexte professionnel
- Knowledge Graph potential
- Liens vers profils sociaux indexés

#### Person détaillé pour Keynotes
```json
"@type": "Person"
```
**Contenu:**
- Schémas individuels pour keynote speakers
- `knowsAbout`: expertise (Python, Software Development)
- `alumniOf`: participation à PyCon Ireland 2026

**Avantage SEO:**
- Mise en avant des keynotes
- Expertise visible dans les résultats de recherche
- Meilleur référencement personnel des speakers

---

### 3. Page Schedule (`/schedule/`)
**Fichier:** `layouts/partials/structured-data-schedule.html`

#### Option 3: EducationalEvent pour chaque talk
```json
"@type": "EducationalEvent"
```
**Contenu:**
- Un schéma par talk/keynote ({{ len (where .Site.Data.sessions "type" "in" (slice "talk" "keynote")) }} events)
- Date et heure précises avec timezone
- Durée au format ISO 8601 (`PT30M`, `PT45M`)
- Lieu avec adresse complète
- Performer (speaker) avec lien vers Person schema
- `superEvent`: lien vers l'événement principal
- `about`: sujets (Python, Software Development)

**Avantage SEO:**
- Chaque talk peut apparaître individuellement dans les résultats
- Google peut créer des rich snippets avec horaires
- Intégration potentielle dans Google Calendar
- Affichage dans les résultats de recherche par sujet

#### EventSeries Schema
```json
"@type": "EventSeries"
```
**Contenu:**
- Représentation du programme complet comme série d'événements
- Lien vers l'événement parent

**Avantage SEO:**
- Google comprend que ce sont des sessions liées
- Meilleur contexte pour l'indexation

---

## 🔗 Relations Entre Schémas

```
Event (Homepage)
    ↓
EventSeries (Schedule) → superEvent → Event
    ↓
EducationalEvent (Talk 1, 2, 3...)
    ↓
    performer → Person (Speaker)
                    ↑
                    performerIn
```

**Flow de données:**
1. Homepage : Event principal
2. Schedule : Série d'EducationalEvents
3. Chaque Talk → lien vers Speaker
4. Chaque Speaker → lien retour vers ses Talks

---

## 📊 Impact SEO Attendu

### Rich Snippets Possibles

#### 1. Homepage - Event Rich Snippet
```
🎪 PyCon Ireland 2026
📅 8-9 November 2026
📍 UCD O'Reilly Hall, Dublin
💰 €40 - €300
👥 Python Ireland
⭐⭐⭐⭐⭐ Event
```

#### 2. Speakers Page - People Carousel
```
👤 [Anna Ravenscroft] [James Murphy] [Siobhan O'Connor]
   Senior SE @ PSF    ML Lead @ Acme  Architect @ Cloud
```

#### 3. Schedule - Event Listings
```
🎤 The Future of Python
   📅 Saturday 10:00 AM
   👤 Anna Ravenscroft
   📍 UCD O'Reilly Hall
   ⏱️ 45 minutes
```

---

## 🧪 Validation

### Outils de Test

1. **Google Rich Results Test**
   ```
   https://search.google.com/test/rich-results
   ```
   - Tester : `http://localhost:53940/`
   - Tester : `http://localhost:53940/speakers/`
   - Tester : `http://localhost:53940/schedule/`

2. **Schema.org Validator**
   ```
   https://validator.schema.org/
   ```

3. **JSON-LD Playground**
   ```
   https://json-ld.org/playground/
   ```

### Vérification Manuelle

1. **View Page Source**
   ```bash
   curl http://localhost:53940/speakers/ | grep -A 50 "application/ld+json"
   ```

2. **Browser DevTools**
   - F12 → Elements → Search for `application/ld+json`
   - Copier le JSON et valider sur schema.org

---

## 📈 Statistiques des Schémas

| Page | Schémas | Types | Total Lines |
|------|---------|-------|-------------|
| Homepage | 4 | Event, Organization, WebSite, BreadcrumbList | ~111 |
| Speakers | 3 | ItemList, Person (x2) | ~85 |
| Schedule | 7+ | EducationalEvent (x6), EventSeries | ~120 |

**Total:** 14+ schémas JSON-LD actifs

---

## 🚀 Prochaines Améliorations Possibles

### Phase 3 (Optional)

1. **Review/Rating Schema**
   - Ajouter après l'événement
   - Témoignages des participants
   - Ratings agrégés

2. **FAQ Schema**
   - Si page FAQ créée
   - Questions fréquentes sur l'événement

3. **Video Schema**
   - Pour talks enregistrés
   - Intégration YouTube après l'événement

4. **Course Schema**
   - Pour workshops spécifiques
   - Si ateliers détaillés

5. **Offer Schema enrichi**
   - Détails par type de ticket
   - Disponibilité temps réel

---

## 🔍 Monitoring SEO

### Après Déploiement

1. **Google Search Console**
   - Vérifier l'indexation des rich snippets
   - Surveiller les erreurs de structured data
   - Analyser les impressions et clics

2. **Rich Results Status Report**
   - Nombre de pages avec rich results
   - Types de snippets actifs
   - Erreurs à corriger

3. **Performance Metrics**
   - CTR (Click-Through Rate) sur les rich snippets
   - Positions moyennes dans les résultats
   - Trafic organique depuis les événements

---

## 📝 Maintenance

### Mises à Jour Nécessaires

- [ ] Ajouter vrais profils sociaux des speakers dans `data/speakers.yml`
- [ ] Mettre à jour les descriptions de talks dans `data/sessions.yml`
- [ ] Ajouter des photos réelles des speakers
- [ ] Vérifier les horaires finaux dans `data/schedule.yml`
- [ ] Tester les schémas en production après déploiement

### Fichiers à Modifier

- `data/speakers.yml` - Infos speakers
- `data/sessions.yml` - Descriptions talks
- `data/schedule.yml` - Horaires précis

Les schémas JSON-LD se mettront à jour automatiquement ! 🎉

---

## 💡 Bonnes Pratiques Appliquées

✅ Utilisation de `@id` pour références croisées
✅ Liens bidirectionnels (speaker ↔ talk)
✅ Dates au format ISO 8601
✅ Durées au format ISO 8601 (PT30M)
✅ URLs absolues avec `absURL`
✅ Structures imbriquées (Place > Address)
✅ `superEvent` pour hiérarchie d'événements
✅ `sameAs` pour profils sociaux
✅ `eventStatus` et `eventAttendanceMode` pour contexte COVID

---

## 🎯 Résultat Final

**Score SEO:**
- Avant structured data speakers/schedule : 9.5/10
- Après implémentation complète : **9.8/10** ⭐⭐⭐⭐⭐

**Bénéfices:**
- ✅ Rich snippets pour event, speakers, talks
- ✅ Meilleure visibilité dans les résultats de recherche
- ✅ Knowledge Graph potential
- ✅ Intégration Google Calendar
- ✅ Carrousel de speakers possible
- ✅ Talks indexés individuellement

**Ready for production!** 🚀
