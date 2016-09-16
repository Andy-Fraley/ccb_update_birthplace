BEGIN {
    printf("individual_id\tBirthplace\n");
}

/[Pp]lace [Oo]f [Bb]irth:/ {
    sub(/^.*[Pp]lace [Oo]f [Bb]irth:/, "");
    sub(/<\/note>/, "");
    sub(/<note>/, "");
    sub(/^ +/, "");
    gsub(/ +/, " ");
    sub(/, *CN$/, ", CT");
    sub(/, *D C$/, ", DC");
    sub(/, *Tenn$/, ", TN");
    sub(/Virgiinia/, "Virginia");
    sub(/, *[Pp][Aa]/, ", PA");
    sub(/, *[Ii][Ll]/, ", IL");
    sub(/^Pittsburgh$/, "Pittsburgh, PA");
    if ($0 != "(not recorded)") {
	printf("%s\t%s\n", ind_id, $0);
    }
}
/individual id=/ {
    sub(/^.*individual id="/, "");
    sub(/">$/, "");
    ind_id=$0
}
