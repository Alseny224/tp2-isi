
echo "Generation de la clé de chiffrement RSA"

openssl genrsa -out prive.key 2048

echo "Clé generé..................."

echo "Affichage des composante p,q,n,e,d"

openssl rsa -in prive.key -text -noout

echo "Chiffrement du fichier........................"

openssl pkey -in prive.key -pubout -out public.pem

openssl pkeyutl -encrypt -pubin -inkey public.pem -in "$1" -out out.enc

echo "fichier chiffré.................."

cat out.enc
echo "Déchiffrement du fichier..."

openssl pkeyutl -decrypt -inkey prive.key -in out.enc -out message_dechiffre.txt

echo "Message déchiffré :"

cat message_dechiffre.txt
