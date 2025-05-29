# Blog über Fortschritte und Versuche

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
