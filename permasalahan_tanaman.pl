% Predikat untuk mengecek apakah sebuah gejala ada dalam daftar gejala yang diamati oleh pengguna
has_symptom(Symptom, SymptomList) :-
    member(Symptom, SymptomList). 

% --- Aturan Diagnosis ---
% Format: diagnose(DaftarGejalaYangDiamati, Diagnosis) :- KondisiGejala.

% Kekurangan Nitrogen
diagnose(SymptomList, 'Kekurangan Nitrogen') :-
    has_symptom(daun_menguning_merata, SymptomList),
    has_symptom(pertumbuhan_terhambat, SymptomList).

% Serangan Kutu Daun (Aphids)
diagnose(SymptomList, 'Serangan Kutu Daun (Aphids)') :-
    has_symptom(kehadiran_serangga_kecil_di_daun, SymptomList),
    has_symptom(daun_keriting_atau_melengkung, SymptomList),
    has_symptom(ada_zat_lengket_di_daun, SymptomList). % Honeydew

% Penyakit Jamur (Powdery Mildew)
diagnose(SymptomList, 'Penyakit Jamur (Powdery Mildew)') :-
    has_symptom(lapisan_putih_seperti_tepung_di_daun, SymptomList).

% Kekurangan Air
diagnose(SymptomList, 'Kekurangan Air') :-
    has_symptom(tanaman_layu, SymptomList),
    \+ has_symptom(kehadiran_serangga_kecil_di_daun, SymptomList), % Tidak ada serangga kecil
    \+ has_symptom(lapisan_putih_seperti_tepung_di_daun, SymptomList). % Tidak ada jamur putih

% Kelebihan Air (Root Rot)
diagnose(SymptomList, 'Kelebihan Air (Root Rot)') :-
    has_symptom(tanaman_layu, SymptomList), % Layu meskipun tanah basah
    has_symptom(tanah_selalu_basah, SymptomList),
    has_symptom(akar_berbau_busuk, SymptomList).