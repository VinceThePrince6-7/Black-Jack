Velkommen til Ege og Vaupels Blackjack med epsilon greedy q learning!

Der er ingen ekstra libraries påkrævet for kørsel af kode.
Måske skal .env rettes til, alt efter hvordan filerne bliver downloadet.

Ellers er dette koden, præcist som vi har kørt.
I BJ_final, kan deck størrelse ændres og det er også her man slår randomiseret deck til hvis q læringen ikke skal tælle.
MIN_CARDS_BEFORE_SHUFFLE = 11 da vi kørte den men dette kan ramme en error hvis dealer løber tør for kort før spillet er færdigt. Alt vores data er kørt ud fra dette, hvor vi så har genstartet træningen hvis fejl opstod men dette kan opjusteres hvis fejl fortsætter. Vi anbefaler et sted mellem 11-15
Det kan være en god ide at ændre training episodes hvis det tager for lang tid at træne, og evaluation episodes ligeså.
