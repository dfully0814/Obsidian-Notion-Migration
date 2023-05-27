const fileSync = require("fs");

const {markdownToBlocks, markdownToRichText} = require('@tryfabric/martian');

function main() {
    return markdownToBlocks(process.argv[2]);
}

const output = main();
console.log(JSON.stringify(output))