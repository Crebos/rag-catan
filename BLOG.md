# Blog über Fortschritte und Versuche

## Entwicklungsumgebung

Da ich lokal auf einer Windows machine arbeite, und die integration von Python und package managers und juypter eher "unschön" ist (um es nett zu formulieren), habe ich mich entschieden mit Lightning Studio zu arbeiten. Dies gibt mir eine Online Umgebung, mit allem wichtigen vorinstalliert.

## Plain and easy

Erster Versuch war mit möglichst standard tools und Einstellungen das PDF auszulesen, tokenizen, embedden und daraus output zu generieren. Dies war erfolgreich aber die Qualität war schon beim ersten Versuch extrem schlecht. Bei einem kurzen Blick in die generierten Chunks (raw PDF output) war schnell klar, dass der pdfplumber die Texte komplett falsch ausgelesen hat. Er hat hier kein Layout berücksichtigt und Linie um Linie ausgelesen, was nicht einmal zu einem korrekten Satz geführt hat.

Dementsprechend war auch der outcome des indexes und der Queries unbrauchbar.

## Advanced Layout parsing

Als nächstes musste ich daher die PDF auslesung optimieren. Hier war die Hoffnung dass mithilfe von pdfplumbers Layout option, das Layout korrekt interpretiert werden konnte. Dann aus dessen output würde man dann die Headings extrahieren und versuchen einzelne Paragraphen zusammenzustellen. Das auseinanderparsen und mit Regex versuchen Regelmässigkeiten über alle Dokumente zusammenzustellen war schwierig und deshalb mithilfe von LLMs gemacht worden. Leider aber war auch hier das Problem, dass Texte nicht immer zusammenhängen waren, und der pdfplumber die Texte verschnitten hat. Auch dies führte zu einer beinahe unbrauchbaren basis text, bei dem es keinen Sinn macht diesen zu tokenizen und embedded. Shit in, shit out :D

Beispiel:

query = "I have all the necessary resources and it is my turn. Where can I place a city? Anywhere connected to a road, right?"

Result #1 (Distance: 0.9765)
you cannot build a city directly. you can onlycontent : to make the sequence easier to learn for beginners. (...)

Interpretation: Hier hat er den string "you cannot build a city directly. you can only" als Heading interpretiert und leider genau im richtigen Satz abgeschnitten. Alles danach ist gibberish. Aber dass er anhand von diesem kleinen Text aus dem index diesen snippet extrahieren konnte, zeigt dass der rest relativ solide läuft.

## Fokuswechsel

Damit ich nicht zu viel Zeit verschwende um das PDF auszulesen, werde ich vorerst die Applikation lauffähig machen. Gemäss Auftragsdokument ist die Qualität des Models nicht die höchste Priorität, sondern der Prozess um ein RAG zu erstellen. Ein nächster Schritt wäre hier, das Chunking zu verbessern, da ich aktuell per Wordcount chunke, und danach nochmals nach tokencount. Könnte man vereinheitlichen.

Um das auslesen aus dem PDF später zu verbessern, kann ich mir vorstellen ein LLM zu verwenden (welches aber etwas schwierig ist, da die Dokumente nicht gerade klein sind) oder ausschau nach einer dynamischeren Library zu halten, welche mehr Optionen für das Auslesen der PDFs gibt.

## Chunking

Mit mehr Fokus auf das Chunking, habe ich festgestellt, dass das maximal limit für das ausgewählte Modell bei 256 immernoch relativ gross ist. Die Aussagen und informationen in den Dokumenten sind sehr kompakt, was eher für kleinere Chunking grössen spricht. Daher probiere ich schrittweise die Grösse etwas zu reduzieren. Dabei vergleiche ich die Chunks und lese quer, unwiefern unrelevante Informationen im selben Chunk gelandet sind. Auch teste ich manuell einzeln was der FAISS Index mir für meine Query geben würde.

Hierbei habe ich gemerkt, dass meine TestQueries noch optimiert werden könnte, da ich aktuell nur eine verwende und diese eher schwierig ist. Ich werde hier total 6 Queries zusammenstellen, dabei jeweils 2 aus je 3 Dokumenten. Diese nutze ich dann um manuell zu prüfen, ob die Antworten in die richtige Richtung gehen.

Diese verwendete ich bis anhin:
query = "I have all the necessary resources and it is my turn. Where can I place a city? Anywhere connected to a road, right?"

Neu verwende ich folgende Fragen:
query = "How do you acquire resources during the game?" # Answer in catan_base_3to4p.pdf at page 11 (you gotta dice the numbers where your settlements are)
query = "How do you get the Longest Road special card and what happens if another player builds a longer road?" # Answer in catan_base_3to4p.pdf at page 5 (5 continoous reoad segments (and longest))
query = "What do you need to play a Seafarers 5-6 Player scenario?" # Answer in catan_seafarers_5to6p.pdf at page 2 (you need Catan & Catan 5&6p, and seafarers game)
query = "How should you assemble the game board for a Seafarers scenario?" # Answer in catan_seafarers_5to6p.pdf at page 2 (Assemble frame as in the photo and place tiles ..)
query = "What happens when the barbarian ship reaches Catan?" # Answer in catan_barbarians_3to4p.pdf at page 7 (must compare knight strength to barbarians strength)
query = "How are knights used in the game, and what actions can they perform?" # Answer in catan_barbarians_3to4p.pdf at page 6 (msut be activated by paying 1 grain, then he can used)

Auch mit chunk size 128 und overlap 24 scheinen mir die Chunks und aussagen noch viel zu durchmischt, mit vielen irrelevanten informationen. Auch die Resultate aus dem Index sind nicht wirklich nutzbar, aber dennoch sind "manchmal" nahe an der tatsächlichen relevanten Stellen.

Mit extremer chunk size 52 und overlap 8 gibts einfach zu wenig Inhalt und verständlichen Kontext. Die Resultate sind nochmals einiges schlechter, wahrscheinlich da der Kontext einfach fehlt, um was es überhaupt geht. Er scheint mehr Wörter zu mappen als inhaltliche Aussagen.

Daher bleibe ich nun mal bei ewtas zwischendurch: chunksize 112 overlap 22

## LLM integration und Gradio Frontend

Da es sich bei der Arbeit mehr um das Chunking und vectorisieren handeln sollte, habe ich für das Frontend und Deployment eine einfache Lösung gewählt. Als Framework habe ich mich für Gradio entschieden, da dies alles was ich brauche out-of-the-box bereitstellt. Detailliertes Customizing brauche ich nicht. Zusätzlicher Bonus ist, dass LLMs relativ gut darin sind, Gradio Frontend zu generieren, was mir den Prozess einiges erleichtert.

Das Frontend über das Studio laufen zu lassen hat nach 1-2 manuellen fixes direkt funktioniert. Die Resultate sind trotz unschönem Chunking .. dennoch relativ hilfreich bei vielen retrieved chunks. Bei k 1-4 sind die Ergebnisse eher schlecht, da die relevante info nicht dabei ist. Wenn man aber auf k 7-10 hochdrückt, ist die gesuchte information in allen beispielen vorhanden, und das LLM kann eine hilfreiche Antwort daraus generieren. Da beim Dokument auslesen die Texte "verschnitten" sind (zwei parallele Paragraphen ausgelesen linie um linie), sind die Sätze verstreut über mehrere Chunks. Ich kann mir vorstellen dass beim inkludieren von vielen Chunks, diese Texte im Prompt wieder zusammenkommen, woraus das LLM dann eine korrekte Antwort generieren kann.

query: Can I move the robber back to the same tile?

k = 2:
"Based on the provided text, the rules for moving the robber are not fully explained. The text mentions (...)"

k = 8:
"No, you cannot move the robber back to the same hex it currently occupies. This is explicitly stated in several of the provided text excerpts [6]."

## Query Rewriting

Da die vectorsearch im FAISS Index nur funktioniert, wenn der Input auch effektiv semantisch nahe ist, zum indexierten Text, habe ich das RAG mit Query Rewriting optimiert.

Zum testen habe ich folgende Query verwendet:

query = "Can I move the weird guy that lets me steal a card from someone, into a water thingy on the map?"

Wobei klar (etwas übertriebene) falsche Begriffe verwendet werden:

- "weird guy that lets me steal a card from someone" = "robber"
- "water thingy" = "hex tile containing water"
- "map" = "game board"

Ohne Query Rewriting versteht es den Kontext erst ab k = 8+, darunter kann er die Regel nicht korrekt wiedergeben.

Mit Query Rewriting hat das LLM mit k = 3 den Kontext verstanden und eine korrekte Antwort generieren können. Hierbei erklärte das LLM auch, dass es mit "robber" den "weird guy" meint.

Beim Prompt für das Query rewriting war wichtig, hier effektiv zu erwähnen nur eine Query zurückzugeben, keine Optionen oder Erklärungen, da das LLM dies sonst macht und was zu schlechteren Resultaten führen könnte.

Das Query Rewriting hat hier eine Verbesserung geliefert, für komisch formulierte inputs.
