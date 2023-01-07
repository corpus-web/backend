"use strict"; (self["webpackChunkylk"] = self["webpackChunkylk"] || []).push([[443], { 9989: function (t, e, i) { i.r(e), i.d(e, { default: function () { return l } }); i(7658); var a = function () { var t = this, e = t._self._c; return e("div", { staticClass: "home", staticStyle: { width: "76.8rem", margin: "auto", border: "1px solid #e5e5e5" } }, [e("my-header"), e("div", { staticClass: "body1" }, [e("div", { staticClass: "swiper-container" }, [e("el-carousel", { attrs: { trigger: "click", height: "26rem", "indicator-position": "none" } }, t._l(t.bannerList, (function (t, i) { return e("el-carousel-item", { key: i }, [e("img", { attrs: { src: t.pictureurl, id: "img" } })]) })), 1)], 1)]), t._m(0), t._m(1), e("div", { staticStyle: { display: "flex", "padding-right": "1rem" } }, [e("div", { staticClass: "button", on: { click: function (e) { return t.$router.push("/Search") } } }, [t._v(" Go Searching ")])]), e("my-footer")], 1) }, s = [function () { var t = this, e = t._self._c; return e("div", { staticClass: "introduce" }, [e("div", { staticClass: "title1" }, [t._v(" Corpus of Shipbuilding and Oceanography Engineering and Nuclear Science ")]), e("div", { staticClass: "title1" }, [t._v(" (COSON) ")]), e("div", { staticClass: "title2" }, [t._v(" -Size of COSON as of 9th September, 2022: Around 9 million words- ")]), e("div", { staticClass: "content" }, [t._v(" COSON is based on the school-based characteristics of Harbin Engineering University, aiming to collect English research papers published in high-impact international journals from 2016 to 2020, containing of around 9 million words and covering the discipline of Shipbuilding and Oceanography Engineering and Nuclear Science. The text sampling taxonomy for the corpus follows the Chinese National System of Level One Disciplines for Degree Educational. The principle of sample selection takes into account the authority and impact factors of the journals, and the selected journals are all SCI international journals, and the impact factors are high in the discipline. ")])]) }, function () { var t = this, e = t._self._c; return e("div", { staticClass: "Mindmapping" }, [e("img", { attrs: { src: i(7514), alt: "Mind mapping" } })]) }], r = { name: "HomeView", created() { this.getbannerList() }, data() { return { bannerList: [] } }, methods: { getbannerList() { this.$axios.request({ method: "GET", url: "/api/corpus/main" }).then((t => { 200 == t.status && (this.bannerList = t.data) })) } } }, n = r, c = i(1001), o = (0, c.Z)(n, a, s, !1, null, null, null), l = o.exports }, 3542: function (t, e, i) { i.r(e), i.d(e, { default: function () { return l } }); var a = function () { var t = this, e = t._self._c; return e("div", { staticClass: "context" }, [e("div", { staticClass: "graybox" }, [t._v(" " + t._s(t.par) + " ")])]) }, s = [], r = { props: ["par"], data() { return { text: "" } } }, n = r, c = i(1001), o = (0, c.Z)(n, a, s, !1, null, "2dc3403b", null), l = o.exports }, 6951: function (t, e, i) { i.r(e), i.d(e, { default: function () { return l } }); var a = function () { var t = this, e = t._self._c; return e("div", { staticClass: "frequency" }, [e("el-table", { staticStyle: { width: "76.8rem", "text-align": "center" }, attrs: { data: t.currentPageData, border: "", height: "19.7rem", "header-cell-style": { background: "rgba(231, 230, 230, 1)", color: "#606266", fontSize: "1rem" } }, on: { "row-click": t.rowclick } }, [e("el-table-column", { attrs: { prop: "id", label: "No.", width: "180", align: "center" } }), e("el-table-column", { attrs: { prop: "fname", label: "Filename", width: "180", align: "center" } }), e("el-table-column", { attrs: { prop: "fline", label: "Solution 1 to 50   Page ", align: "center" }, scopedSlots: t._u([{ key: "default", fn: function (i) { return [e("span", { domProps: { innerHTML: t._s(t.setkey(i.row.fline)) } })] } }]) })], 1), e("div", { staticClass: "pagination" }, [e("div", { staticClass: "firstpage", on: { click: t.firstpage } }, [t._v(" |< ")]), e("div", { staticClass: "firstpage", on: { click: t.prevPage } }, [t._v(" < ")]), e("div", { staticClass: "firstpage", on: { click: t.nextPage } }, [t._v(" > ")]), e("div", { staticClass: "firstpage", on: { click: t.lastPage } }, [t._v(" >| ")]), e("div", { staticClass: "buttondark", staticStyle: { width: "20%", "margin-left": "5%", cursor: "pointer" }, on: { click: t.showpage } }, [t._v(" Show Page ")]), e("input", { directives: [{ name: "model", rawName: "v-model", value: t.showp, expression: "showp" }], staticClass: "pagenum", attrs: { placeholder: "" }, domProps: { value: t.showp }, on: { input: function (e) { e.target.composing || (t.showp = e.target.value) } } }), e("div", { staticClass: "buttondark", staticStyle: { cursor: "pointer", width: "30%", "margin-left": "18%", "margin-right": "1%" }, on: { click: t.change } }, [t._v(" " + t._s(t.order) + " ")])])], 1) }, s = [], r = { props: ["longtext", "resindexnum", "indexnum", "currentPageData"], data() { return { pageSize: 1, currentPage: 1, headPage: 1, showp: "", order: "Random Order", orderway: 1 } }, mounted() { this.p(), console.log(this.pageSize) }, methods: { p() { this.pageSize = Math.ceil(this.resindexnum / this.indexnum) }, getCurrentPageData() { this.$axios.request({ method: "GET", url: "/api/corpus/article", params: { word: this.longtext, max_num: this.indexnum, current_page: this.currentPage } }).then((t => { this.$message({ showClose: !0, message: "开始检索……", type: "success" }), this.currentPageData = t.data.data })) }, firstpage() { this.currentPage = this.headPage, this.getCurrentPageData() }, prevPage() { if (1 == this.currentPage) return !1; this.currentPage--, this.getCurrentPageData() }, nextPage() { if (console.log("下一页"), this.currentPage == this.pageSize) return !1; this.currentPage++, this.getCurrentPageData() }, lastPage() { if (this.currentPage == this.pageSize) return !1; this.currentPage = this.pageSize, this.getCurrentPageData() }, showpage() { this.currentPage = this.showp, this.getCurrentPageData(), console.log(this.showp) }, change() { "Show Corpus" == this.order ? (this.order = "Random Order", this.orderway = 1, this.getCurrentPageData()) : (this.order = "Show Corpus", this.orderway = 2, this.getCurrentPageData()) }, setkey(t) { return t.includes(this.longtext) ? (t = t.replace(this.longtext, '<font style="color:rgba(47, 85, 151, 1)!important;">' + this.longtext + "</font>"), t) : t }, rowclick(t) { console.log(t.id), this.$emit("jump", t.fpar) } } }, n = r, c = i(1001), o = (0, c.Z)(n, a, s, !1, null, null, null), l = o.exports }, 2532: function (t, e, i) { i.r(e), i.d(e, { default: function () { return d } }); var a = function () { var t = this, e = t._self._c; return e("div", { staticClass: "about", staticStyle: { width: "76.8rem", margin: "auto", border: "1px solid #e5e5e5" } }, [e("my-header"), e("my-image"), e("div", { staticClass: "menu" }, [e("div", { class: [t.searchclick ? t.click : t.unclick], on: { click: t.search } }, [t._v(" Serch ")]), e("div", { class: [t.frequencyclick ? t.click : t.unclick], on: { click: t.frequency } }, [t._v(" Frequency ")]), e("div", { class: [t.contextclick ? t.click : t.unclick], on: { click: t.context } }, [t._v(" Context ")])]), e("div", { staticClass: "content" }, [t.searchclick ? e("div", { staticClass: "search" }, [e("div", { staticClass: "graybox" }, [e("textarea", { directives: [{ name: "model", rawName: "v-model", value: t.longtext, expression: "longtext" }], attrs: { id: "longinput", placeholder: "add multiple lines" }, domProps: { value: t.longtext }, on: { input: function (e) { e.target.composing || (t.longtext = e.target.value) } } }), e("div", { staticClass: "buttonbox" }, [e("div", { staticClass: "buttonlight", staticStyle: { width: "62%", cursor: "pointer" }, on: { click: t.startsearch } }, [t._v(" Start Searching ")]), e("div", { staticClass: "buttonlight", staticStyle: { width: "32%", cursor: "pointer" }, on: { click: t.reset } }, [t._v(" Reset ")])]), e("div", { staticClass: "selectionbox" }, [e("div", { staticClass: "tickbox" }, [e("input", { directives: [{ name: "model", rawName: "v-model", value: t.limitcase, expression: "limitcase" }], attrs: { type: "checkbox", id: "checkbox" }, domProps: { checked: Array.isArray(t.limitcase) ? t._i(t.limitcase, null) > -1 : t.limitcase }, on: { change: function (e) { var i = t.limitcase, a = e.target, s = !!a.checked; if (Array.isArray(i)) { var r = null, n = t._i(i, r); a.checked ? n < 0 && (t.limitcase = i.concat([r])) : n > -1 && (t.limitcase = i.slice(0, n).concat(i.slice(n + 1))) } else t.limitcase = s } } }), e("div", { staticClass: "buttondark", staticStyle: { width: "62%" } }, [t._v(" Case-sensitive ")])]), e("div", { staticClass: "tickbox" }, [e("div", { staticClass: "buttondark", staticStyle: { width: "62%", "margin-right": "0.8rem" } }, [t._v(" Search window size ")]), e("select", { directives: [{ name: "model", rawName: "v-model", value: t.bothnum, expression: "bothnum" }], attrs: { id: "selectbox" }, on: { change: function (e) { var i = Array.prototype.filter.call(e.target.options, (function (t) { return t.selected })).map((function (t) { var e = "_value" in t ? t._value : t.value; return e })); t.bothnum = e.target.multiple ? i : i[0] } } }, [e("option", { attrs: { disabled: "", value: "" } }), e("option", [t._v("50")]), e("option", [t._v("75")]), e("option", [t._v("100")]), e("option", [t._v("125")]), e("option", [t._v("150")])])]), e("div", { staticClass: "tickbox" }, [e("div", { staticClass: "buttondark", staticStyle: { width: "62%", "margin-right": "0.8rem" } }, [t._v(" Number of hits per page ")]), e("select", { directives: [{ name: "model", rawName: "v-model", value: t.indexnum, expression: "indexnum" }], attrs: { id: "selectbox" }, on: { change: function (e) { var i = Array.prototype.filter.call(e.target.options, (function (t) { return t.selected })).map((function (t) { var e = "_value" in t ? t._value : t.value; return e })); t.indexnum = e.target.multiple ? i : i[0] } } }, [e("option", { attrs: { disabled: "", value: "" } }), e("option", [t._v("50")]), e("option", [t._v("100")]), e("option", [t._v("150")])])]), e("div", { staticClass: "tickbox" }, [e("div", { staticClass: "buttondark", staticStyle: { width: "62%", "margin-right": "0.8rem" } }, [t._v(" Save list ")]), e("select", { directives: [{ name: "model", rawName: "v-model", value: t.saveyes, expression: "saveyes" }], attrs: { id: "selectbox" }, on: { change: function (e) { var i = Array.prototype.filter.call(e.target.options, (function (t) { return t.selected })).map((function (t) { var e = "_value" in t ? t._value : t.value; return e })); t.saveyes = e.target.multiple ? i : i[0] } } }, [e("option", { attrs: { disabled: "", value: "" } }), e("option", [t._v("Yes")]), e("option", [t._v("No")])])])])]), t._m(0)]) : t.frequencyclick ? e("div", { staticClass: "frequency" }, [e("frequency", { attrs: { currentPageData: t.currentPageData, longtext: t.longtext, indexnum: t.indexnum, resindexnum: t.resindexnum }, on: { jump: t.jump } })], 1) : t.contextclick ? e("div", { staticClass: "context" }, [e("context", { attrs: { par: t.par } })], 1) : t._e()]), e("my-footer")], 1) }, s = [function () { var t = this, e = t._self._c; return e("div", { staticClass: "graybox1" }, [e("div", { staticClass: "graysmall", staticStyle: { "margin-top": "2rem" } }, [t._v(" Case-Sensitive determines whether The result and the result would be two different searches, or It finds, it finds, It Finds. ")]), e("div", { staticClass: "graysmall" }, [t._v(" Search Window Size refers to the number of characters on either side of the search word. ")]), e("div", { staticClass: "graysmall" }, [t._v(" Number of Hits per Page means the number of hits that you have searched in one page. ")])]) }], r = i(6951), n = i(3542), c = { components: { frequency: r["default"], context: n["default"] }, data() { return { searchclick: !0, frequencyclick: !1, contextclick: !1, click: "click", unclick: "unclick", longtext: "", limitcase: !1, bothnum: 50, indexnum: 50, resindexnum: "", saveyes: "", currentPageData: [], par: "" } }, methods: { search() { this.searchclick = !0, this.frequencyclick = !1, this.contextclick = !1 }, frequency() { this.searchclick = !1, this.frequencyclick = !0, this.contextclick = !1 }, context() { this.searchclick = !1, this.frequencyclick = !1, this.contextclick = !0 }, startsearch() { this.$axios.request({ method: "GET", url: "/api/corpus/article", params: { word: this.longtext, window_size: this.bothnum, max_num: this.indexnum } }).then((t => { this.$message({ showClose: !0, message: "开始检索……", type: "success" }), this.currentPageData = t.data.data, this.resindexnum = t.data.total })), this.searchclick = !1, this.frequencyclick = !0, this.contextclick = !1 }, reset() { this.longtext = "" }, jump(t) { console.log(t), this.par = t, this.searchclick = !1, this.frequencyclick = !1, this.contextclick = !0 } } }, o = c, l = i(1001), u = (0, l.Z)(o, a, s, !1, null, null, null), d = u.exports }, 7514: function (t, e, i) { t.exports = i.p + "img/Mindmapping.399e114b.png" } }]);
//# sourceMappingURL=about.cac7e538.js.map